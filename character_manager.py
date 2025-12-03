"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module

Name: Joshua Evans

AI Usage: Assisted in completing missing functions and fixing logic structure. AI also assisted in explaining lines of code.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER CREATION
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class.
    """

    # Dictionary of valid classes and their base stats
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    # Prevent using a class that does not exist
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(
            f"Invalid class '{character_class}'. "
            f"Valid classes: {', '.join(valid_classes.keys())}" #takes all the valid classes from the dictionary and joins them, Python is looking for a comma to separate each value.
        )

    base = valid_classes[character_class]  # select base stats

    # Return the new character dictionary
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

# ============================================================================
# SAVE / LOAD
# ============================================================================

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file following strict formatting.
    """

    # Ensure save directory exists
    os.makedirs(save_directory, exist_ok=True) #os.makedirs creates directories. python creaates the folder and the parent folders if needed.

    # Build the file path
    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename) #os.path.join-> joins paths depending on what OS you are on.

    # Convert lists into comma-separated strings
    inventory_str = ",".join(character["inventory"])
    active_str = ",".join(character["active_quests"])
    completed_str = ",".join(character["completed_quests"])

    # Write all fields in fixed format
    file_content = (
        f"NAME: {character['name']}\n"
        f"CLASS: {character['class']}\n"
        f"LEVEL: {character['level']}\n"
        f"HEALTH: {character['health']}\n"
        f"MAX_HEALTH: {character['max_health']}\n"
        f"STRENGTH: {character['strength']}\n"
        f"MAGIC: {character['magic']}\n"
        f"EXPERIENCE: {character['experience']}\n"
        f"GOLD: {character['gold']}\n"
        f"INVENTORY: {inventory_str}\n"
        f"ACTIVE_QUESTS: {active_str}\n"
        f"COMPLETED_QUESTS: {completed_str}\n"
    )

    # Save into the file
    with open(filepath, "w") as f:
        f.write(file_content)

    return True


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file.
    """

    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    # Ensure the file actually exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"No save file for '{character_name}'")

    # Read file safely
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Could not read file")

    # Parse key-value pairs into a dictionary
    data = {}
    for line in lines:
        if not line.strip():
            continue

        if ":" not in line:
            raise InvalidSaveDataError("Malformed line in save file")

        parts = line.strip().split(":", 1)
        
        if len(parts) != 2:
            raise InvalidSaveDataError("Malformed line in save file")

        key = parts[0].strip()
        value = parts[1].strip()
        data[key] = value

    # Convert data into character dictionary
    try:
        character = {
            "name": data["NAME"],
            "class": data["CLASS"],
            "level": int(data["LEVEL"]),
            "health": int(data["HEALTH"]),
            "max_health": int(data["MAX_HEALTH"]),
            "strength": int(data["STRENGTH"]),
            "magic": int(data["MAGIC"]),
            "experience": int(data["EXPERIENCE"]),
            "gold": int(data["GOLD"]),
            "inventory": data["INVENTORY"].split(",") if data["INVENTORY"] else [],
            "active_quests": data["ACTIVE_QUESTS"].split(",") if data["ACTIVE_QUESTS"] else [],
            "completed_quests": data["COMPLETED_QUESTS"].split(",") if data["COMPLETED_QUESTS"] else []
        }
    except KeyError:
        raise InvalidSaveDataError("Missing fields in save file")
    except ValueError:
        raise InvalidSaveDataError("Invalid numeric data in save file")

    # Ensure data types are valid
    validate_character_data(character)
    return character

# ============================================================================
# SAVE FILE UTILITIES
# ============================================================================

def list_saved_characters(save_directory="data/save_games"):
    """
    Return list of saved character names (without _save.txt)
    """

    # If no directory exists, nothing is saved
    if not os.path.exists(save_directory):
        return []

    names = []
    # Go through all save files and strip "_save.txt"
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            names.append(filename[:-9])  # remove suffix

    return names


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file.
    """

    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    # File must exist to delete it
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"'{character_name}' does not exist.")

    os.remove(filepath)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    # Prevent gaining XP while dead
    if character["health"] <= 0:
        raise CharacterDeadError("Dead characters cannot gain XP.")

    character["experience"] += xp_amount  # add XP

    # Perform level-ups (can happen multiple times)
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1

        # Increase stats when leveling
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2

        # Restore HP to full
        character["health"] = character["max_health"]


def add_gold(character, amount):
    # Prevent gold from going negative
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Not enough gold.")

    character["gold"] = new_total
    return new_total


def heal_character(character, amount):
    # Store the old HP to return how much was healed
    old_hp = character["health"]
    character["health"] = min(character["health"] + amount, character["max_health"])
    return character["health"] - old_hp


def is_character_dead(character):
    # Dead if health is 0 or lower
    return character["health"] <= 0


def revive_character(character):
    # Cannot revive someone already alive
    if character["health"] > 0:
        return False

    # Bring back with half HP
    character["health"] = character["max_health"] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    # Required fields that must exist
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

    # Fields that must be numeric
    numeric_fields = [
        "level", "health", "max_health", "strength",
        "magic", "experience", "gold"
    ]

    for key in numeric_fields:
        if not isinstance(character[key], (int, float)): #checks if the character[key] is not an int and also checks if its not a float.
            raise InvalidSaveDataError(f"{key} must be numeric")

    # Fields that must be lists
    list_fields = ["inventory", "active_quests", "completed_quests"]

    for key in list_fields:
        if not isinstance(character[key], list): #checks if the character[key] is not a list
            raise InvalidSaveDataError(f"{key} must be a list")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    # Example test character
    c = create_character("TestHero", "Warrior")
    save_character(c)
    loaded = load_character("TestHero")
    print("Loaded character:", loaded)
