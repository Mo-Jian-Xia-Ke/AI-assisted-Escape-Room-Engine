from enum import Enum
class Room:
    def __init__(self, items):
        self.items = items

class Item:
    def __init__(self, id, visible, pickable, locked, interactive, arg, success):
        self.id = id
        self.visible = visible
        self.pickable = pickable
        self.interactive = interactive
        self.locked = locked
        self.arg = arg
        self.success = success

    def interact(self, item_list):
        # Maybe add pull and push afterwards?
        if self.interactive == Interactive.INVESTIGATE:
            item_list[self.arg].visualize()
        if self.interactive == Interactive.WITH_ITEM:
            item_list[self.id].unlock()
    
    def visualize(self):
        self.visible = True

    def devisualize(self):
        self.visible = False

    def unlock(self):
        self.locked = False
        if self.success:
            print("Success")


class Interactive(Enum):
    NONE = 0
    INVESTIGATE = 1
    WITH_ITEM = 2