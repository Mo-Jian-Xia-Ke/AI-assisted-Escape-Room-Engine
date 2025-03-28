from enum import Enum
class Room:
    def __init__(self, items):
        self.items = items

class Item:
    def __init__(self, id, name, state_num, visible, pickable, locked, interactive, arg, success, object_type):
        self.id = id
        self.name = name
        self.state_num = state_num
        self.visible = visible
        self.pickable = pickable
        self.interactive = interactive
        self.locked = locked
        self.arg = arg
        self.success = success
        self.feedback_map = {}

        self.label_list = [f'look at the {name}']
        if object_type == 'KEY':
            self.label_list.append(f'use the {name}')
        elif object_type == 'LOCK':
            self.label_list.append(f'unlock the {name}')
        elif object_type == 'CONTAINER':
            self.label_list.append(f'open the {name}')
            self.label_list.append(f'close the {name}')
            self.label_list.append(f'push the {name}')
            self.label_list.append(f'pull the {name}')
        elif object_type == 'INVESTIGATABLE':
            self.label_list.append(f'investigate the {name}')

    def get_name(self):
        return self.name
    
    def add_feedback(self, index, feedback):
        self.feedback_map.update({index: feedback})

    def get_feedback(self, index):
        return self.feedback_map.get(index)
    
    def change_state(self, state_num):
        self.state_num = state_num

    def get_state(self):
        return self.state_num

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