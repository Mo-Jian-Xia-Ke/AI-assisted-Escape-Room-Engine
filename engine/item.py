import enum

class ItemType(enum.Enum):
    NORMAL = "normal"
    PUZZLE = "puzzle"

class Item:
    # Note that the first item has id of 1, in this case
    counter = 0

    """
    id: the item's position (+1) in the item list
    name: the item's name
    states: the array of states the item has
    state_num: indicates the state the item is in
    i_type: the item's type (of Enum ItemType)
    puzzle_state: the state_num where the puzzle should be displayed to the player
    """
    def __init__(self, name, states, i_type=ItemType.NORMAL, puzzle_state=0, code_states=[]):
        self.id = Item._set_id()
        self.name = name
        self.states = states
        self.state_num = 0
        self.i_type = i_type
        self.puzzle_state = puzzle_state
        self.code_states = code_states
    
    def _set_id():
        Item.counter += 1
        return Item.counter

    def set_puzzle(self, puzzle):
        assert self.i_type == ItemType.PUZZLE, f"Item '{self.name}' should contain a puzzle!"
        self.puzzle = puzzle
    
    def get_name(self):
        return self.name
    
    def get_state_list(self):
        return self.states
    
    def get_state_num(self):
        return self.state_num
    
    def get_type(self):
        return self.i_type
    
    def get_current_state(self):
        return self.states[self.state_num]
    
    def get_current_label(self):
        return self.get_current_state().get_label()
    
    def set_current_label(self, label):
        self.get_current_state().set_label(label)
    
    def get_description(self):
        return self.get_current_state().get_description()
    
    def get_room_description(self):
        return self.get_current_state().get_room_description()
    
    def set_room_description(self, input):
        self.get_current_state().set_room_description(input)

    # May throw IndexError
    def get_next_state(self):
        try:
            next_state = self.states[self.state_num + 1]
        except IndexError:
            print("No further states!")
        return next_state

    def check_invisible(self):
        return self.get_current_state().check_invisible()
    
    # Check whether the current state is the end state of the item
    def check_end_state(self):
        return self.state_num == len(self.states) - 1

    # Check whether the item can be proceed to the next state
    def check_proceeding_status(self):
        return not self.check_end_state() and self.get_current_state().check_proceeding_status()
    
    # Proceed the item's state, then awake items in the new state's awaken_list
    def proceed_state(self):
        if self.check_proceeding_status():
            self.state_num += 1
            self.get_current_state().awake_all()
    
# ------- ItemType.PUZZLE ------- #

    def get_puzzle_state_num(self):
        return self.puzzle_state
    
    def get_code_states(self):
        return self.code_states

    def check_display_status(self):
        return self.state_num == self.puzzle_state
    
    def check_code_status(self):
        code_ready = True
        for depend_pair in self.code_states:
            code_item = depend_pair[0]
            code_state_num = depend_pair[1]
            if code_item.get_state_num() < code_state_num:
                code_ready = False
                break
        return code_ready

    # If the state is the puzzle-displaying state, display the puzzle attached to the item
    def display_puzzle(self):
        assert self.i_type == ItemType.PUZZLE, f"Item '{self.name}' should contain a puzzle!"
        if self.check_display_status():
            return self.puzzle.display()

# ------- [Debug only] ------- #
    def print_states(self):
        for i, state in enumerate(self.states):
            print(f"{i}: {state}")