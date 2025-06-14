# Project name:
AI-assisted escape room engine

# Author
Cheng Ma

# Project Type:
Imperial College London's BEng Individual Project

# Requirements:
Required packages are shown in requirements.txt.
In order to run your game, you should install them in advance.

# Third-Party Libraries:
Third-party library uses are documented in NOTICE.

# Guide:
1. When creating the room, create your new folder which contains your own item_config.JSON and puzzle_config.JSON.
2. Create an initializer.py that calls the start_game() function in the engine/main_engine.py
3. Modify the main.py from the highest layer to call your initializer.py
4. Run the main program in the outer level (the level that you can directly see main.py) to start playing your own room

# Customization:
You can modify and create your own puzzles within in the puzzles folder. There are some templates for you to follow.

# Structure:
Core Components:
    engine:
        - item
        - state
        - action
        - generators
        - hint system
    puzzles:
        - puzzle
        - dependent_puzzles:
            - ...
        - independent_puzzles:
            - ...
    - simple_room_demo:
        - item_config.JSON
        - puzzle_config.JSON
        - initializer.py