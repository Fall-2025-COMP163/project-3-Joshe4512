"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Completed
Name: Joshua Evans 
AI Usage: Gemini helped code the game state portion and the Game Loop portion.

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
    """
    # TOPIC: Loops (While)
    while True:
        print("\n--- MAIN MENU ---")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        
        # TOPIC: Strings & Types
        choice_input = input("Enter your choice: ")
        
        # TOPIC: Exceptions
        try:
            choice = int(choice_input)
            
            # TOPIC: Branching (If/Elif/Else)
            if choice == 1:
                return 1
            elif choice == 2:
                return 2
            elif choice == 3:
                return 3
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("That is not a number. Please try again.")

def new_game():
    """
    Start a new game
    """
    # TOPIC: Variables (Global)
    global current_character, game_running
    
    print("\n--- NEW GAME ---")
    
    # TOPIC: Loops & Strings
    name = ""
    while name == "":
        name = input("Enter your character's name: ")
        if name == "":
            print("Name cannot be empty.")

    class_choice = ""
    while class_choice == "":
        print("Classes: Warrior, Mage, Rogue")
        class_choice = input("Enter character class: ")
        
        # TOPIC: Exceptions & Functions
        try:
            # We call the function from the imported module
            current_character = character_manager.create_character(name, class_choice)
            print("Character created successfully!")
            
            # Start the game loop
            game_running = True
            game_loop()
            
        except InvalidCharacterClassError:
            print("Error: That is not a valid class name.")
            class_choice = "" # Reset to force loop to continue
        except Exception:
            print("An unknown error occurred creating the character.")
            return

def load_game():
    """
    Load an existing saved game
    """
    global current_character, game_running
    
    print("\n--- LOAD GAME ---")
    
    # TOPIC: Files
    # Since we can't use 'os' module to list files (advanced),
    # we ask the user for the name of their save file.
    filename = input("Enter the character name to load: ")
    
    try:
        # Calls the function that handles file reading internally
        current_character = character_manager.load_character(filename)
        print("Game loaded successfully!")
        
        game_running = True
        game_loop()
        
    except FileNotFoundError:
        print("Could not find a save file for that character.")
    except SaveFileCorruptedError:
        print("Error: The save file data is corrupted.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running
    
    # TOPIC: Loops
    while game_running == True:
        choice = game_menu()
        
        # TOPIC: Branching
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
            print("Goodbye!")
            game_running = False # Ends the loop

def game_menu():
    """
    Display game menu and get player choice
    """
    print("\n=========================")
    # TOPIC: Classes (Accessing attributes of the object)
    print("Player: " + current_character.name) 
    print("=========================")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    
    while True:
        user_input = input("Choose an action (1-6): ")
        try:
            choice = int(user_input)
            if choice >= 1 and choice <= 6:
                return choice
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print("\n--- STATS ---")
    # TOPIC: Classes (Using the __str__ method of the class)
    print(current_character)
    
    # Check for active quests
    active_count = 0
    # TOPIC: Loops (Iterating through a dictionary)
    for quest_id in current_character.active_quests:
        active_count = active_count + 1
    
    print("Active Quests: " + str(active_count))

def view_inventory():
    """Display and manage inventory"""
    global current_character
    
    print("\n--- INVENTORY ---")
    # Call module function
    inventory_system.display_inventory(current_character)
    
    print("Options: [1] Use Item, [2] Equip Item, [3] Back")
    choice = input("Choice: ")
    
    if choice == "1":
        item_name = input("Enter item name to use: ")
        try:
            inventory_system.use_item(current_character, item_name)
            print("Used " + item_name)
        except ItemNotFoundError:
            print("You don't have that item.")
            
    elif choice == "2":
        item_name = input("Enter item name to equip: ")
        try:
            inventory_system.equip_item(current_character, item_name)
            print("Equipped " + item_name)
        except Exception:
            print("Could not equip item.")

def quest_menu():
    """Quest management menu"""
    # Simplified for starter code
    print("\n--- QUESTS ---")
    quest_handler.view_quests(current_character)

def explore():
    """Find and fight random enemies"""
    global current_character, game_running
    
    print("\n--- EXPLORING ---")
    # TOPIC: Inheritance
    # combat_system will treat current_character the same way 
    # regardless of if it is a Warrior, Mage, or Rogue class.
    
    try:
        # Returns True if player wins, False if player dies
        result = combat_system.start_random_encounter(current_character)
        
        if result == True:
            print("You won the battle!")
        else:
            handle_character_death()
            
    except Exception:
        print("An error occurred during combat.")

def shop():
    """Shop menu for buying/selling items"""
    global current_character
    
    print("\n--- SHOP ---")
    print("Gold: " + str(current_character.gold))
    print("1. Buy Health Potion (50g)")
    print("2. Back")
    
    choice = input("Choice: ")
    if choice == "1":
        if current_character.gold >= 50:
            current_character.gold = current_character.gold - 50
            inventory_system.add_item(current_character, "Health Potion")
            print("Purchased Health Potion.")
        else:
            print("Not enough gold.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    # TOPIC: Files and Exceptions
    try:
        character_manager.save_character(current_character)
        print("Game saved.")
    except Exception:
        print("Failed to save game file.")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Creating defaults...")
        game_data.create_default_data_files()
        # Try loading one more time
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print("\nYOU HAVE DIED.")
    print("1. Revive (Costs Gold)")
    print("2. Quit")
    
    choice = input("Choose: ")
    if choice == "1":
        # Revive logic
        current_character.health = 10
        current_character.gold = 0
        print("You have been revived.")
    else:
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("==================================================")
    print("   QUEST CHRONICLES")
    print("==================================================")
    print("Welcome! Prepare for adventure.")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    display_welcome()
    
    # Load initial data
    try:
        load_game_data()
    except InvalidDataFormatError:
        print("Critical Error: Game data is corrupted.")
        return # Exit the function
        
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Exiting game.")
            break # Exit the loop

if __name__ == "__main__":
    main()
