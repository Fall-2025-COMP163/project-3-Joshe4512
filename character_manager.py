"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module

Name: Joshua Evans

AI Usage: Assisted in completing missing functions and fixing logic structure.
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

    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    if character_class not in valid_classes:
        raise InvalidCharacterClassError(
            f"Invalid class '{character_class}'. "
            f"Valid classes: {', '.join(valid_classes.keys())}"
        )

    base = valid_classes[character_class]

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
    os.makedirs(save_directory, exist_ok=True)

    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # Convert lists
    inventory_str = ",".join(character["inventory"])
    active_str = ",".join(character["active_quests"])
    completed_str = ",".join(character["completed_quests"])

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

    with open(filepath, "w") as f:
        f.write(file_content)

    return True


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file.
    """
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"No save file for '{character_name}'")

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Could not read file")

    # Parse file
    data = {}
    for line in lines:
        if ":" not in line:
            raise InvalidSaveDataError("Malformed line in save file")

        key, value = line.strip().split(": ", 1)
        data[key] = value

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

    validate_character_data(character)
    return character

# ============================================================================
# SAVE FILE UTILITIES
# ============================================================================

def list_saved_characters(save_directory="data/save_games"):
    """
    Return list of saved character names (without _save.txt)
    """
    if not os.path.exists(save_directory):
        return []

    names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            names.append(filename[:-9])  # remove "_save.txt"

    return names


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file.
    """
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"'{character_name}' does not exist.")

    os.remove(filepath)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError("Dead characters cannot gain XP.")

    character["experience"] += xp_amount

    # Multiple level-ups possible
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]


def add_gold(character, amount):
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Not enough gold.")

    character["gold"] = new_total
    return new_total


def heal_character(character, amount):
