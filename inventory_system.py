"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Completed Code

Name: [Joshua Evans]
AI Usage: Assisted in completing TODO functions
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    character["inventory"].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found")
    character["inventory"].remove(item_id)
    return True

def has_item(character, item_id):
    return item_id in character["inventory"]

def count_item(character, item_id):
    return character["inventory"].count(item_id)

def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character["inventory"])

def clear_inventory(character):
    removed = character["inventory"].copy()
    character["inventory"].clear()
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")

    if "type" not in item_data or "effect" not in item_data:
        raise InvalidItemTypeError("Item data is invalid")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Item is not consumable")

    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)

    character["inventory"].remove(item_id)
    return f"Used {item_data.get('name', item_id)} and gained {stat} +{value}"

def equip_weapon(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")
    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon")

    if character.get("equipped_weapon"):
        unequip_weapon(character)

    stat, value = parse_item_effect(item_data["effect"])
    character[stat] += value

    character["equipped_weapon"] = item_id
    character["inventory"].remove(item_id)

    return f"Equipped weapon {item_data.get('name', item_id)} (+{value} {stat})"

def equip_armor(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")
    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor")

    if character.get("equipped_armor"):
        unequip_armor(character)

    stat, value = parse_item_effect(item_data["effect"])
    character[stat] += value

    character["equipped_armor"] = item_id
    character["inventory"].remove(item_id)

    if stat == "max_health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    return f"Equipped armor {item_data.get('name', item_id)} (+{value} {stat})"

def unequip_weapon(character):
    weapon = character.get("equipped_weapon")
    if weapon is None:
        return None
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full; cannot unequip")

    return_id = weapon
    item_effect = character["item_data"][weapon]["effect"]
    stat, value = parse_item_effect(item_effect)

    character[stat] -= value
    character["inventory"].append(weapon)
    character["equipped_weapon"] = None

    return return_id

def unequip_armor(character):
    armor = character.get("equipped_armor")
    if armor is None:
        return None
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full; cannot unequip")

    return_id = armor
    item_effect = character["item_data"][armor]["effect"]
    stat, value = parse_item_effect(item_effect)

    character[stat] -= value
    if stat == "max_health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    character["inventory"].append(armor)
    character["equipped_armor"] = None

    return return_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    if "cost" not in item_data:
        raise InvalidItemTypeError("Item data missing cost")

    cost = item_data["cost"]
    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold")
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    character["gold"] -= cost
    character["inventory"].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not found")

    sell_price = item_data["cost"] // 2
    character["inventory"].remove(item_id)
    character["gold"] += sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    stat, value = effect_string.split(":")
    return stat, int(value)

def apply_stat_effect(character, stat_name, value):
    character[stat_name] += value
    if stat_name == "health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

def display_inventory(character, item_data_dict):
    counts = {}
    for item_id in character["inventory"]:
        counts[item_id] = counts.get(item_id, 0) + 1

    print("\n--- Inventory ---")
    if not counts:
        print("Empty")
        return

    for item_id, qty in counts.items():
        item = item_data_dict.get(item_id, {"name": item_id, "type": "unknown"})
        print(f"{item['name']} ({item['type']}) x{qty}")

    
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

