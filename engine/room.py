
class Room:
    """
    ...
    description: an item-str dict that can be further interpreted into the room description
    """
    def __init__(self, items, puzzles, action_interpreter, end_item, end_state, description=""):
        self.items = items
        self.puzzles = puzzles
        self.action_interpreter = action_interpreter
        self.end_item = end_item
        self.end_state = end_state
        self.description = description
    
    def get_items(self):
        return self.items
    
    def get_puzzles(self):
        return self.puzzles
    
    def get_action_interpreter(self):
        return self.action_interpreter
    
    def get_end_item(self):
        return self.end_item
    
    def get_end_state(self):
        return self.end_state
    
    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description
    
    def set_hint_generator(self, hint_generator):
        self.hint_generator = hint_generator

    def get_hint_generator(self):
        return self.hint_generator
    
    # Check whether the given state is the end state of the game
    def check_end_state(self):
        return self.end_item.get_current_state() == self.end_state