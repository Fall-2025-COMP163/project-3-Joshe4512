"""
COMP 163 - Project 3: Quest Chronicles
Joshua Evans 
AI USAGE: ChatGPT helped with coding the data loading functions and explained what each line meant.
Game Data Module - Completed Code
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)
# imports the os module  which allows file and folder operations like os.path.exists or os.makedirs and imports custom exceptions already made.

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"): #Defines load_quests and shows the default file location if no tests pass)
    """Load quests from file and return dict."""
    if not os.path.exists(filename):
        raise MissingDataFileError("Quest data file missing")
        # Loop that checks if the file exists and if it the file doesnt exists it raises the custom "MissingDataFileError."

    try:
        with open(filename, "r") as f:
            raw = f.read().strip()
    except Exception:
        raise CorruptedDataError("Quest file unreadable")
        # Opens the file safely using with (automatically closes the file).

        # Reads all lines and splits them into a list of strings.

        # If reading fails (permissions, encoding errors), raises CorruptedDataError.

    if not raw:
        raise InvalidDataFormatError("Quest file empty")

    blocks = [b.strip().split("\n") for b in raw.split("\n\n") if b.strip()]
    quests = {} #initializes an empty directory to store quests 
#block collects lines for one quest.

#Loops over each line:

#If line is blank (""), it means one quest finished.

#Sends block to parse_quest_block to turn it into a dictionary.

#Adds the quest to the quests dictionary with the key quest_id.

#Non-blank lines are added to the block.

    for block in blocks:
        quest_dict = parse_quest_block(block)
        validate_quest_data(quest_dict)
        quests[quest_dict["quest_id"]] = quest_dict

    return quests


def load_items(filename="data/items.txt"):
    """Load items from file and return dict."""
    if not os.path.exists(filename):
        raise MissingDataFileError("Item data file missing")

    try:
        with open(filename, "r") as f:
            raw = f.read().strip()
    except Exception:
        raise CorruptedDataError("Item file unreadable")

    if not raw:
        raise InvalidDataFormatError("Item file empty")

    blocks = [b.strip().split("\n") for b in raw.split("\n\n") if b.strip()]
    items = {}

    for block in blocks:
        item_dict = parse_item_block(block)
        validate_item_data(item_dict)
        items[item_dict["item_id"]] = item_dict

    return items


def validate_quest_data(q):
    """Ensure quest dict has required fields and correct types."""
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    for r in required:
        if r not in q:
            raise InvalidDataFormatError("Missing quest field")

    numeric_fields = ["reward_xp", "reward_gold", "required_level"]
    for n in numeric_fields:
        if not isinstance(q[n], int):
            raise InvalidDataFormatError("Quest numeric field invalid")

    return True


def validate_item_data(i):
    """Ensure item dict is valid."""
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for r in required:
        if r not in i:
            raise InvalidDataFormatError("Missing item field")

    if i["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError("Invalid item type")

    if not isinstance(i["cost"], int):
        raise InvalidDataFormatError("Cost must be integer")

    if ":" not in i["effect"]:
        raise InvalidDataFormatError("Invalid effect format")

    return True


def create_default_data_files():
    """Create default quests and items files."""
    try:
        os.makedirs("data", exist_ok=True)

        if not os.path.exists("data/quests.txt"):
            with open("data/quests.txt", "w") as f:
                f.write(
                    "QUEST_ID: starter_quest\n"
                    "TITLE: First Steps\n"
                    "DESCRIPTION: Begin your journey.\n"
                    "REWARD_XP: 50\n"
                    "REWARD_GOLD: 20\n"
                    "REQUIRED_LEVEL: 1\n"
                    "PREREQUISITE: NONE\n"
                )

        if not os.path.exists("data/items.txt"):
            with open("data/items.txt", "w") as f:
                f.write(
                    "ITEM_ID: potion_small\n"
                    "NAME: Small Health Potion\n"
                    "TYPE: consumable\n"
                    "EFFECT: health:20\n"
                    "COST: 10\n"
                    "DESCRIPTION: Restores a small amount of health.\n"
                )

    except Exception:
        raise CorruptedDataError("Unable to create default files")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """Parse quest block into dict."""
    quest = {}
    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError("Bad quest line")

            key, val = line.split(": ", 1)
            key = key.lower()

            if key in ["reward_xp", "reward_gold", "required_level"]:
                val = int(val)

            if key == "quest_id":
                quest["quest_id"] = val
            elif key == "title":
                quest["title"] = val
            elif key == "description":
                quest["description"] = val
            elif key == "reward_xp":
                quest["reward_xp"] = val
            elif key == "reward_gold":
                quest["reward_gold"] = val
            elif key == "required_level":
                quest["required_level"] = val
            elif key == "prerequisite":
                quest["prerequisite"] = val
            else:
                raise InvalidDataFormatError("Unknown quest field")

    except ValueError:
        raise InvalidDataFormatError("Quest number invalid")
    except Exception:
        raise InvalidDataFormatError("Unable to parse quest")

    return quest


def parse_item_block(lines):
    """Parse item block into dict."""
    item = {}
    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError("Bad item line")

            key, val = line.split(": ", 1)
            key = key.lower()

            if key == "cost":
                val = int(val)

            if key == "item_id":
                item["item_id"] = val
            elif key == "name":
                item["name"] = val
            elif key == "type":
                item["type"] = val
            elif key == "effect":
                item["effect"] = val
            elif key == "cost":
                item["cost"] = val
            elif key == "description":
                item["description"] = val
            else:
                raise InvalidDataFormatError("Unknown item field")

    except ValueError:
        raise InvalidDataFormatError("Item number invalid")
    except Exception:
        raise InvalidDataFormatError("Unable to parse item")

    return item
