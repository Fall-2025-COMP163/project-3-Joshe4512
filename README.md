# Quest Chronicles - Text-Based RPG

**Name:** Joshua Evans
**Course:** COMP 163
**Project:** Project 3

## Project Overview

Quest Chronicles is a modular, text-based Role-Playing Game (RPG) written in Python. The game features character creation, persistence (save/load functionality), a turn-based combat system, inventory management, and quest tracking. It demonstrates the integration of multiple custom modules, file I/O operations, and exception handling.

-----

## Module Architecture

The project is organized into a hub-and-spoke architecture where `main.py` acts as the central controller, coordinating data flow between specialized manager modules.

  * **`main.py` (The Controller):**

      * Contains the game loop and main menu logic.
      * Handles all user input and output (print statements).
      * Catches exceptions raised by other modules to prevent crashes.
      * Maintains the global game state (`current_character`, `game_running`).

  * **`character_manager.py`:**

      * Handles the logic for creating specific character classes (Warrior, Mage, Rogue).
      * Manages "backend" logic for leveling up, healing, and gaining XP.
      * Responsible for **File I/O**: Saving and loading character data to `.txt` files using string parsing.

  * **`combat_system.py`:**

      * Contains logic for turn-based battles.
      * Calculates damage and determines victory/defeat conditions.

  * **`inventory_system.py`:**

      * Manages the list of items a character holds.
      * Handles logic for using consumables (potions) or equipping gear.

  * **`custom_exceptions.py`:**

      * Defines specific error classes used across the project to allow for precise error handling.

-----

## Exception Strategy

The project uses a "Fail Fast, Catch Late" strategy. Low-level modules (like `character_manager`) do not print errors; instead, they raise specific custom exceptions. The `main.py` module catches these exceptions to display user-friendly messages.

**Key Exceptions:**

1.  **`InvalidCharacterClassError`**:

      * **When:** Raised during character creation if the user inputs a class (e.g., "Archer") that is not in the allowed dictionary.
      * **Why:** Prevents the game from creating a broken character object with missing stats.

2.  **`SaveFileCorruptedError` / `InvalidSaveDataError`**:

      * **When:** Raised during loading if a save file is missing data, empty, or formatted incorrectly.
      * **Why:** Protects the game from crashing when trying to read a bad file. It allows the main menu to tell the user the file is bad rather than terminating the program.

3.  **`CharacterDeadError`**:

      * **When:** Raised if an action (like gaining XP) is attempted on a character with 0 HP.
      * **Why:** Enforces game logic rules programmatically.

-----

## Design Choices

1.  **Text-Based File Persistence:**

      * I chose to save data in a human-readable text format (Key: Value) rather than binary (Pickle) or JSON.
      * *Justification:* This meets the course requirement for file processing and makes debugging easier, as I can open the save file and manually check if the data is writing correctly.

2.  **State Management via Dictionary:**

      * The character is stored as a dictionary rather than a complex class instance.
      * *Justification:* This simplifies serialization (saving to text) and allows for flexible data manipulation without needing complex getters/setters for every single attribute.

3.  **Separation of Input/Output:**

      * `character_manager.py` contains almost no `input()` or `print()` statements.
      * *Justification:* This separation of concerns allows the logic to be tested automatically (via PyTest) without human intervention. All user interaction is centralized in `main.py`.

-----

## AI Usage

**AI Assistance Used:** Generative AI (ChatGPT/Gemini)
**Scope of Usage:**

  * **Logic Structure:** AI helped structure the main game loop logic in `main.py` to ensure the menu system flowed correctly.
  * **Debugging:** AI assisted in identifying a logic error in `load_character` where file lines were not splitting correctly due to whitespace issues.
  * **Code Explanation:** AI was used to explain specific syntax regarding dictionary manipulation and exception propagation.

-----

## How to Play

1.  **Start the Game:**
    Run the `main.py` file in your terminal:

    ```bash
    python main.py
    ```

2.  **New Game:**

      * Select "New Game" from the main menu.
      * Enter a name and choose a class (Warrior, Mage, or Rogue).

3.  **Gameplay:**

      * **Explore:** Venture out to fight random enemies to gain XP and Gold.
      * **Shop:** Use gold to buy Health Potions.
      * **Inventory:** Use potions to heal if your health gets low.
      * **Save:** Select "Save and Quit" to store your progress.

4.  **Loading:**

      * On restart, select "Load Game" and type the name of your previously saved character to resume.
