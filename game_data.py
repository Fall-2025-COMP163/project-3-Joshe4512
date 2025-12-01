"""
COMP 163 - Project 3: Quest Chronicles
Joshua Evans 
AI USAGE: ChatGPT helped with coding the data loading functions, and Gemini helped further knowledge of code by explaining what each line meant.
Game Data Module 
"""

import os
# Importing custom exceptions from a separate file so we can raise specific errors
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """Load quests from file and return dict."""
    
    # 1. Check if the file exists before trying to open it.
    if not os.path.exists(filename):
        # If the file is missing, stop immediately and raise a specific error.
        raise MissingDataFileError("Quest data file missing")

    try:
        # 2. Open the file in 'read' mode ('r'). 
        # The 'with' statement ensures the file closes automatically when done.
        with open(filename, "r") as f:
            # Read the whole file into one string and remove extra whitespace at start/end.
            raw = f.read().strip()
    except Exception:
        # If opening/reading fails (e.g., permissions, drive error), raise a corrupted error.
        raise CorruptedDataError("Quest file unreadable")

    # 3. Check if the file was technically there but empty inside.
    if not raw:
        raise InvalidDataFormatError("Quest file empty")

    # 4. PARSING LOGIC (The "Chopping" Step):
    # - raw.split("\n\n"): Splits the file into blocks based on blank lines (separating quests).
    # - b.strip().split("\n"): Splits each block into individual lines of text.
    # - if b.strip(): Ignores any accidental empty blocks.
    blocks = [b.strip().split("\n") for b in raw.split("\n\n") if b.strip()]
    
    quests = {} # Initialize an empty dictionary to store the final quest data.

    # 5. Process each block of text.
    for block in blocks:
        # Convert the list of text lines into a dictionary (key: value pairs).
        quest_dict = parse_quest_block(block)
        
        # Check if the dictionary has all required fields and correct data types.
        validate_quest_data(quest_dict)
        
        # Add to the main dictionary using the quest_id as the lookup key.
        quests[quest_dict["quest_id"]] = quest_dict

    return quests


def load_items(filename="data/items.txt"):
    """Load items from file and return dict."""
    # (This function works exactly like load_quests, but for items)

    # Check existence
    if not os.path.exists(filename):
        raise MissingDataFileError("Item data file missing")

    try:
        # Read file
        with open(filename, "r") as f:
            raw = f.read().strip()
    except Exception:
        raise CorruptedDataError("Item file unreadable")

    # Check if empty
    if not raw:
        raise InvalidDataFormatError("Item file empty")

    # Split into blocks (double newline) then lines (single newline)
    blocks = [b.strip().split("\n") for b in raw.split("\n\n") if b.strip()]
    items = {}

    # Parse, validate, and store
    for block in blocks:
        item_dict = parse_item_block(block)   # Uses the item-specific parser
        validate_item_data(item_dict)         # Uses the item-specific validator
        items[item_dict["item_id"]] = item_dict

    return items


def validate_quest_data(q):
    """Ensure quest dict has required fields and correct types."""
    # List of keys that MUST be present in the dictionary.
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    # Check if any required key is missing.
    for r in required:
        if r not in q:
            raise InvalidDataFormatError("Missing quest field")

    # Check if numeric fields actually contain integers (not strings).
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]
    for n in numeric_fields:
        if not isinstance(q[n], int):
            raise InvalidDataFormatError("Quest numeric field invalid")

    return True


def validate_item_data(i):
    """Ensure item dict is valid."""
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    # Check missing keys
    for r in required:
        if r not in i:
            raise InvalidDataFormatError("Missing item field")

    # Verify the item type is one of the allowed categories.
    if i["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError("Invalid item type")

    # Verify cost is a number.
    if not isinstance(i["cost"], int):
        raise InvalidDataFormatError("Cost must be integer")

    # Verify the effect string has a colon (e.g., "health:20").
    if ":" not in i["effect"]:
        raise InvalidDataFormatError("Invalid effect format")

    return True


def create_default_data_files():
    """Create default quests and items files."""
    try:
        # Create the 'data' folder if it doesn't exist. 'exist_ok=True' prevents errors if it does.
        os.makedirs("data", exist_ok=True)

        # If quests.txt is missing, create it and write a starter quest.
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

        # If items.txt is missing, create it and write a starter item.
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
        # If we can't write the files (e.g., disk full, permissions), raise an error.
        raise CorruptedDataError("Unable to create default files")

# ============================================================================
# HELPER FUNCTIONS (PARSERS)
# ============================================================================

def parse_quest_block(lines):
    """Parse quest block into dict."""
    quest = {}
    try:
        for line in lines:
            # Check for data integrity: every line must have a key and value separated by ": "
            if ": " not in line:
                raise InvalidDataFormatError("Bad quest line")

            # Split the line only at the first ": ". 
            # 'key' becomes what's on the left (e.g., "QUEST_ID").
            # 'val' becomes what's on the right (e.g., "starter_quest").
            key, val = line.split(": ", 1)
            key = key.lower() # Normalize the key to lowercase for consistency.

            # If the key is for a number field, convert the string value to an integer.
            if key in ["reward_xp", "reward_gold", "required_level"]:
                val = int(val)

            # Map the parsed data to the correct dictionary key.
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
                # If we encounter a key we don't recognize, raise an error.
                raise InvalidDataFormatError("Unknown quest field")

    except ValueError:
        # Catches errors if int() conversion fails (e.g., "REWARD_XP: fifty")
        raise InvalidDataFormatError("Quest number invalid")
    except Exception:
        # Catches any other unexpected errors during parsing.
        raise InvalidDataFormatError("Unable to parse quest")

    return quest


def parse_item_block(lines):
    """Parse item block into dict."""
    item = {}
    try:
        for line in lines:
            # Check for bad formatting
            if ": " not in line:
                raise InvalidDataFormatError("Bad item line")

            # Split line into Key and Value
            key, val = line.split(": ", 1)
            key = key.lower()

            # Convert Cost to an integer immediately
            if key == "cost":
                val = int(val)

            # Map data to dictionary keys
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
