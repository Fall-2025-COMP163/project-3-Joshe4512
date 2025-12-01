"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Joshua Evans]
AI Usage: simplified logic, ensured compatibility with assignment structure, helped code the random enemy levling 

Handles combat mechanics
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)


# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """Create enemy by type."""
    
    types = {
        "goblin": {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }

    if enemy_type not in types:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")

    return types[enemy_type].copy() #returns the type of enemy and copies it to a new dictionary 


def get_random_enemy_for_level(character_level):
    """Return correct enemy for the level range."""
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """Turn-based combat manager."""
   # Initializes the battle instance with the player, enemy, and starting values.
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("The character is already dead and cannot fight.")

        display_battle_log("Battle begins!")
        display_combat_stats(self.character, self.enemy)

        while self.combat_active:
            display_battle_log(f"--- Turn {self.turn} ---")
            self.player_turn()

        result = self.check_battle_end()
        if result is not None:
            self.combat_active = False
            winner = result
            break

            self.enemy_turn()
            self.turn += 1

        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            display_battle_log(f"You gained {rewards['xp']} XP and {rewards['gold']} gold!")

            self.character["experience"] += rewards["xp"]
            self.character["gold"] += rewards["gold"]

            return {"winner": "player", **rewards}
        else:
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        print("\nYour turn:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run Away")

        choice = input("Choose an action: ")

        if choice == "1":
            dmg = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, dmg)
            display_battle_log(f"You dealt {dmg} damage!")
        elif choice == "2":
            message = use_special_ability(self.character, self.enemy)
            display_battle_log(message)
        elif choice == "3":
            if self.attempt_escape():
                display_battle_log("You escaped successfully!")
                return
            else:
                display_battle_log("Escape failed!")
        else:
            display_battle_log("Invalid choice. Turn wasted.")

        display_combat_stats(self.character, self.enemy)

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError()

        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"{self.enemy['name']} dealt {dmg} damage!")
        display_combat_stats(self.character, self.enemy)

    def calculate_damage(self, attacker, defender):
        raw = attacker["strength"] - (defender["strength"] // 4)
        return max(1, raw)

    def apply_damage(self, target, damage):
        target["health"] = max(0, target["health"] - damage)

    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            return "player"
        if self.character["health"] <= 0:
            return "enemy"
        return None

    def attempt_escape(self):
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    cls = character["class"].lower()

    if cls == "warrior":
        return warrior_power_strike(character, enemy)
    elif cls == "mage":
        return mage_fireball(character, enemy)
    elif cls == "rogue":
        return rogue_critical_strike(character, enemy)
    elif cls == "cleric":
        return cleric_heal(character)
    else:
        return "Your class has no special ability."


def warrior_power_strike(character, enemy):
    dmg = character["strength"] * 2
    enemy["health"] -= dmg
    return f"Power Strike! You dealt {dmg} damage."


def mage_fireball(character, enemy):
    dmg = character["magic"] * 2
    enemy["health"] -= dmg
    return f"Fireball! You scorched the enemy for {dmg} damage."


def rogue_critical_strike(character, enemy):
    if random.random() < 0.5:
        dmg = character["strength"] * 3
        enemy["health"] -= dmg
        return f"Critical Strike! Massive {dmg} damage!"
    else:
        return "Critical Strike failed! No bonus damage."


def cleric_heal(character):
    healed = min(30, character["max_health"] - character["health"])
    character["health"] += healed
    return f"You healed for {healed} HP."


# ============================================================================
# UTILITIES
# ============================================================================

def can_character_fight(character):
    return character["health"] > 0


def get_victory_rewards(enemy):
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }


def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: {character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: {enemy['health']}/{enemy['max_health']}")


def display_battle_log(message):
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

