import json

# sys.path.append(os.path.abspath("../"))
from puzzles import*

config_file = "my_room/puzzle_config.json"
# config_file = "puzzle_config.json"

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
    puzzle_type = _puzzle_type_init(raw_puzzle)
    puzzle = _assign_puzzle(raw_puzzle, puzzle_type)
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

def _puzzle_type_init(raw_puzzle):
    try:
        str_puzzle_dependency = raw_puzzle['puzzle_dependency']
        puzzle_dependency = None
        for dependency in PuzzleDependency:
            if str_puzzle_dependency == dependency.value:
                puzzle_dependency = dependency
        assert puzzle_dependency, "Wrong puzzle dependency!"
    except KeyError:
        puzzle_dependency = None
    try:
        str_p_type = raw_puzzle['type']
        p_type = None
        # Assume DepPuzzleType and IndepPuzzleType do not have collision of same type name (str)
        for puzzle_type in DepPuzzleType:
            if str_p_type == puzzle_type.value:
                p_type = puzzle_type
                break
        for puzzle_type in IndepPuzzleType:
            if str_p_type == puzzle_type.value:
                p_type = puzzle_type
                break
        assert p_type, "Wrong puzzle type!"
        if isinstance(p_type, DepPuzzleType):
            if not puzzle_dependency:
                puzzle_dependency = PuzzleDependency.DEPENDENT_PUZZLE
            assert puzzle_dependency == PuzzleDependency.DEPENDENT_PUZZLE, "Mismatch of puzzle's dependency and type!"
        elif isinstance(p_type, IndepPuzzleType):
            if not puzzle_dependency:
                puzzle_dependency = PuzzleDependency.INDEPENDENT_PUZZLE
            assert puzzle_dependency == PuzzleDependency.INDEPENDENT_PUZZLE, "Mismatch of puzzle's dependency and type!"
    except KeyError:
        print("Missing puzzle type!")
    return p_type

def _assign_puzzle(raw_puzzle, puzzle_type):
    if puzzle_type == DepPuzzleType.DIGITAL_LOCK:
        return digital_lock_init(raw_puzzle)
    else:
        # TODO
        pass

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
    return digital_lock.DigitalLock(name=name, code=code, num_digits=num_digits, title=title)