
class Room:
    """
    ...
    description: an item-str dict that can be further interpreted into the room description
    """
    def __init__(self, items, puzzles, end_state, description={}):
        self.items = items
        self.puzzles = puzzles
        self.end_state = end_state
        self.description = description
    
    def get_items(self):
        return self.items
    
    def get_puzzles(self):
        return self.puzzles
    
    def get_end_state(self):
        return self.end_state
    
    def get_description(self):
        return self.description
    
    # Check whether the given state is the end state of the game
    def check_end_state(self, state):
        return self.end_state == state