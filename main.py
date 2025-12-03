"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Completed
Name: Joshua Evans 
AI Usage: AI helped generate the game loop logic

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *
import sys  # Imported to handle clean exits

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n--- MAIN MENU ---")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ")
            choice = int(choice)
            if 1 <= choice <= 3:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character, game_running
    
    print("\n--- CHARACTER CREATION ---")
    while True:
        name = input("Enter your character's name: ").strip()
        if len(name) > 0:
            break
        print("Name cannot be empty.")

    print("\nClasses available: Warrior, Mage, Rogue")
    while True:
        char_class = input("Enter character class: ").strip().capitalize()
        try:
            # Assumes create_character returns the new character object
            current_character = character_manager.create_character(name, char_class)
            print(f"\nCharacter created! Welcome, {name} the {char_class}.")
            save_game()  # Autosave on creation
            game_loop()
            break
        except InvalidCharacterClassError:
            print(f"Error: '{char_class}' is not a valid class. Please try Warrior, Mage, or Rogue.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    print("\n--- LOAD GAME ---")
    # Assumes character_manager has a function to list save files
    # If not, you might need to use os.listdir() here
    try:
        saves = character_manager.get_available_saves() 
        if not saves:
            print("No saved games found.")
            return

        print("Available Saves:")
        for i, save_name in enumerate(saves, 1):
            print(f"{i}. {save_name}")

        selection = input("\nEnter name of character to load: ").strip()
        current_character = character_manager.load_character(selection)
        print(f"\nWelcome back, {current_character.name}!")
        game_loop()
        
    except FileNotFoundError:
        print("Save file not found.")
    except SaveFileCorruptedError:
        print("Error: Save file is corrupted and cannot be loaded.")
    except Exception as e:
        print(f"Error loading game: {e}")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to Main Menu...")
            game_running = False
        
        # Autosave after significant actions is often good practice
        # save_game()

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("\n" + "="*30)
    print(f"Playing as: {current_character.name}")
    print("="*30)
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")
    
    while True:
        try:
            choice = int(input("\nChoose an action (1-6): "))
            if 1 <= choice <= 6:
                return choice
            print("Please choose a number between 1 and 6.")
        except ValueError:
            print("Invalid input.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    # Assumes your character class has a __str__ method or similar display function
    print("\n--- CHARACTER STATS ---")
    print(current_character) 
    
    # Assuming quest_handler tracks active quest count
    active_count = quest_handler.get_active_quest_count(current_character)
    print(f"Active Quests: {active_count}")

def view_inventory():
    """Display and manage inventory"""
    global current_character
    
    print("\n--- INVENTORY ---")
    # Assumes inventory_system has a display function
    inventory_system.display_inventory(current_character)
    
    print("\nOptions: [U]se Item, [E]quip Item, [B]ack")
    choice = input("Choice: ").upper()
    
    if choice == 'U':
        item_name = input("Item to use: ")
        try:
            inventory_system.use_item(current_character, item_name)
            print(f"Used {item_name}.")
        except ItemNotFoundError:
            print("You don't have that item.")
        except InvalidItemTypeError:
            print("That item cannot be used.")
            
    elif choice == 'E':
        item_name = input("Item to equip: ")
        try:
            inventory_system.equip_item(current_character, item_name)
            print(f"Equipped {item_name}.")
        except Exception as e: # Catch-all for equipment errors
            print(f"Could not equip: {e}")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    print("\n--- QUEST JOURNAL ---")
    print("1. View Active Quests")
    print("2. Back")
    
    choice = input("Choice: ")
    if choice == '1':
        quest_handler.show_active_quests(current_character)
    # Expand logic here to accept new quests from all_quests if needed

def explore():
    """Find and fight random enemies"""
    global current_character
    
    print("\n--- EXPLORING ---")
    print("You venture into the wild...")
    
    # Assumes combat_system handles the logic of generating an enemy
    # and running the turn-based loop
    try:
        victory = combat_system.start_random_encounter(current_character)
        
        if victory:
            print("You were victorious! Gained XP and Gold.")
            # combat_system might handle rewards internally, or you do it here:
            # current_character.gain_xp(100)
        else:
            handle_character_death()
            
    except Exception as e:
        print(f"Error during combat: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    print("\n--- GENERAL STORE ---")
    print(f"Your Gold: {current_character.gold}")
    print("1. Buy Potions (50 gold)")
    print("2. Leave")
    
    choice = input("Choice: ")
    if choice == '1':
        if current_character.gold >= 50:
            current_character.gold -= 50
            # Assumes inventory_system handles adding
            inventory_system.add_item(current_character, "Health Potion")
            print("Bought Health Potion!")
        else:
            print("Not enough gold!")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    if current_character:
        try:
            character_manager.save_character(current_character)
            print("Game saved successfully.")
        except Exception as e:
            print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # Using generic placeholders, replace with your actual data loading logic
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Generating defaults...")
        game_data.create_default_data_files()
        # Retry loading
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print("\nYOU HAVE DIED.")
    print("1. Revive (Costs 50% Gold)")
    print("2. Quit Game")
    
    choice = input("Choice: ")
    if choice == '1':
        # Assumes a revive method exists
        current_character.health = current_character.max_health
        current_character.gold = int(current_character.gold * 0.5)
        print("You have been revived at the cost of your fortune.")
    else:
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("      QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except InvalidDataFormatError as e:
        print(f"CRITICAL ERROR loading game data: {e}")
        print("Please check data files for errors.")
        sys.exit(1) # Exit program if data is broken
    except Exception as e:
        print(f"Unexpected error during startup: {e}")
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
