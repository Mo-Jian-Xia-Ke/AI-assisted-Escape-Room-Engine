import json
import sys
sys.path.append('../puzzles')

import digital_lock
from puzzle import Puzzle_type

# config_file = "my_room/puzzle_config.json"
config_file = "puzzle_config.json"

# Given the path to the config file, return the initialized system (merge puzzles in items)
def system_init(config_file, items):
    with open(config_file, "r") as f:
        data = json.load(f)
    return puzzle_dict_init(data, items)

# Given a list json, initialize the item-puzzle dict, while also bind the puzzle as a field of the item
def puzzle_dict_init(data, items):
    puzzles = {}
    for i in range(len(data)):
        belong_item, puzzle = puzzle_init(data[i], items)
        belong_item.set_puzzle(puzzle)
        puzzles[belong_item] = puzzle
    return puzzles

# Given a json object, initialize the puzzle according to the extracted puzzle type
# Return a tuple of belong_item and the initialized puzzle object
def puzzle_init(raw_puzzle, items):
    belong_item_name = belong_item_init(raw_puzzle)
    belong_item = items[belong_item_name]
    try:
        type_value = raw_puzzle['type']
        p_type = None
        type_value = raw_puzzle['type']
        for puzzle_type in Puzzle_type:
            if type_value == puzzle_type.value:
                p_type = puzzle_type
        assert p_type, "Wrong puzzle type!"
    except KeyError:
        print("Missing puzzle type!")

    if puzzle_type == Puzzle_type.DIGITAL_LOCK:
        puzzle = digital_lock_init(raw_puzzle)

    return (belong_item, puzzle)

# Extract puzzle name
def name_init(raw_puzzle):
    try:
        name = raw_puzzle['name']
    except KeyError:
        print("Missing puzzle name!")
    return name

# Extract puzzle's belonging item
def belong_item_init(raw_puzzle):
    try:
        belong_item = raw_puzzle['belong_item']
    except KeyError:
        print("Missing belonging item!")
    return belong_item

# ------- Different initialization for different puzzles ------- #

# Initialize the digital_lock puzzle
def digital_lock_init(raw_puzzle):
    name = name_init(raw_puzzle)
    try:
        code = raw_puzzle['code']
    except KeyError:
        code = "1234"
    num_digits = len(code)
    try:
        title = raw_puzzle['title']
    except KeyError:
        title = name
    return digital_lock.Digital_Lock(name=name, code=code, num_digits=num_digits, title=title)