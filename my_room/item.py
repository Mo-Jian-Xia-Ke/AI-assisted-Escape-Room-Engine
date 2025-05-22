import enum

class Item_type(enum.Enum):
    NORMAL = "normal"
    PUZZLE = "puzzle"

class Room:
    def __init__(self, items):
        self.items = items

class Item:
    # Note that the first item has id of 1, in this case
    counter = 0

    """
    id: the item's position (+1) in the item list
    name: the item's name
    states: the array of states the item has
    state_num: indicates the state the item is in
    i_type: the item's type (of Enum Item_type)
    puzzle_state: the state_num where the puzzle should be displayed to the player
    """
    def __init__(self, name, states, i_type=Item_type.NORMAL, puzzle_state=0):
        self.id = Item.__set_id__()
        self.name = name
        self.states = states
        self.state_num = 0
        self.i_type = i_type
        self.puzzle_state = puzzle_state
    
    def __set_id__():
        Item.counter += 1
        return Item.counter

    def set_puzzle(self, puzzle):
        assert self.i_type == Item_type.PUZZLE, f"Item '{self.name}' should contain a puzzle!"
        self.puzzle = puzzle
    
    def get_name(self):
        return self.name
    
    def get_state_list(self):
        return self.states
    
    def get_state_num(self):
        return self.state_num
    
    def get_type(self):
        return self.i_type
    
    def get_puzzle_state_num(self):
        return self.puzzle_state
    
    def get_current_state(self):
        return self.states[self.state_num]
    
    def get_current_label(self):
        return self.get_current_state().get_label()
    
    def set_current_label(self, label):
        self.get_current_state().set_label(label)

    def check_invisible(self):
        return self.get_current_state().check_invisible()
    
    # Check whether the current state is the end state of the item
    def check_end_state(self):
        return self.state_num == len(self.states) - 1

    # Check whether the item can be proceed to the next state
    def check_proceeding_status(self):
        return self.get_current_state().check_proceeding_status()
    
    # Proceed the item's state, then awake items in the new state's awaken_list
    def proceed_state(self):
        if self.check_proceeding_status():
            self.state_num += 1
            self.get_current_state().awake_all()
    
    def check_display_status(self):
        return self.state_num == self.puzzle_state

    # If the state is the puzzle-displaying state, display the puzzle attached to the item
    def display_puzzle(self):
        assert self.i_type == Item_type.PUZZLE, f"Item '{self.name}' should contain a puzzle!"
        if self.check_display_status():
            return self.puzzle.display()

    # [Debug only]
    def print_states(self):
        for i, state in enumerate(self.states):
            print(f"{i}: {state}")

###########


    
#     def add_feedback(self, index, feedback):
#         self.feedback_map.update({index: feedback})

#     def get_feedback(self, index):
#         return self.feedback_map.get(index)
    
#     def change_state(self, state_num):
#         self.state_num = state_num

#     def get_state(self):
#         return self.state_num

#     def interact(self, item_list):
#         # Maybe add pull and push afterwards?
#         if self.interactive == Interactive.INVESTIGATE:
#             item_list[self.arg].visualize()
#         if self.interactive == Interactive.WITH_ITEM:
#             item_list[self.id].unlock()
    
#     def visualize(self):
#         self.visible = True

#     def devisualize(self):
#         self.visible = False

#     def unlock(self):
#         self.locked = False
#         if self.success:
#             print("Success")


# class Interactive(Enum):
#     NONE = 0
#     INVESTIGATE = 1
#     WITH_ITEM = 2