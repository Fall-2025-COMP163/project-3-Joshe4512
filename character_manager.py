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

# =================
