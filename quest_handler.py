"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Joshua Evans]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest.
    """
    # Checks if quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found")

    quest = quest_data_dict[quest_id]
    required_level = quest.get("required_level", 1)
    prereq = quest.get("prerequisite", "NONE")

    # Check level requirement
    if character["level"] < required_level:
        raise InsufficientLevelError("Character level too low")

    # Check prerequisite
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError("Prerequisite quest not completed")

    # Check not already completed
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError("Quest already completed")

    # Check not already active
    if quest_id in character["active_quests"]:
        raise QuestAlreadyCompletedError("Quest already completed or already active")

    # Accept quest
    character["active_quests"].append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards.
    """
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found")

    # Check quest is active
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active")

    quest = quest_data_dict[quest_id]

    # Remove from active, add to completed
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    reward_xp = quest.get("reward_xp", 0)
    reward_gold = quest.get("reward_gold", 0)

    # Reward the character manually (no character_manager in tests)
    character["experience"] = character.get("experience", 0) + reward_xp
    character["gold"] = character.get("gold", 0) + reward_gold

    return {
        "xp": reward_xp,
        "gold": reward_gold
    }


def abandon_quest(character, quest_id):
    """
    Abandon an active quest.
    """
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active")

    character["active_quests"].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    return [quest_data_dict[q] for q in character["active_quests"] if q in quest_data_dict]


def get_completed_quests(character, quest_data_dict):
    return [quest_data_dict[q] for q in character["completed_quests"] if q in quest_data_dict]


def get_available_quests(character, quest_data_dict):
    available = []
    for qid, quest in quest_data_dict.items():
        # Skip completed
        if qid in character["completed_quests"]:
            continue

        # Skip active
        if qid in character["active_quests"]:
            continue

        # Level requirement
        if character["level"] < quest.get("required_level", 1):
            continue

        # Prerequisite
        prereq = quest.get("prerequisite", "NONE")
        if prereq != "NONE" and prereq not in character["completed_quests"]:
            continue

        available.append(quest)

    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character["completed_quests"]


def is_quest_active(character, quest_id):
    return quest_id in character["active_quests"]


def can_accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]

    if character["level"] < quest.get("required_level", 1):
        return False

    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        return False

    if quest_id in character["completed_quests"]:
        return False

    if quest_id in character["active_quests"]:
        return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found")

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            raise QuestNotFoundError("Prerequisite quest does not exist")

        chain.insert(0, current)
        prereq = quest_data_dict[current].get("prerequisite", "NONE")

        if prereq == "NONE":
            break

        current = prereq

    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    if total == 0:
        return 0.0

    completed = len(character["completed_quests"])
    return (completed / total) * 100


def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = 0
    total_gold = 0

    for qid in character["completed_quests"]:
        if qid in quest_data_dict:
            quest = quest_data_dict[qid]
            total_xp += quest.get("reward_xp", 0)
            total_gold += quest.get("reward_gold", 0)

    return {"total_xp": total_xp, "total_gold": total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [
        q for q in quest_data_dict.values()
        if min_level <= q.get("required_level", 1) <= max_level
    ]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Level Requirement: {quest_data['required_level']}")
    print(f"XP Reward: {quest_data['reward_xp']}")
    print(f"Gold Reward: {quest_data['reward_gold']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")


def display_quest_list(quest_list):
    for q in quest_list:
        print(f"{q['title']} (Lvl {q['required_level']}) - XP: {q['reward_xp']}, Gold: {q['reward_gold']}")


def display_character_quest_progress(character, quest_data_dict):
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== Quest Progress ===")
    print(f"Active: {len(character['active_quests'])}")
    print(f"Completed: {len(character['completed_quests'])}")
    print(f"Completion: {percent:.2f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    for qid, quest in quest_data_dict.items():
        prereq = quest.get("prerequisite", "NONE")
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"Prerequisite '{prereq}' for quest '{qid}' does not exist"
            )

    return True



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

