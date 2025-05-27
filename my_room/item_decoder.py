import state
import item
import json

# config_file = "my_room/item_config.json"
config_file = "item_config.json"

# Given the path to the config file, return the initialized system (item dict)
def system_init(config_file):
    with open(config_file, "r") as f:
        data = json.load(f)
    return item_dict_init(data)

# Given a list json, initialize the item dict
def item_dict_init(data):
    items = {}
    for i in range(len(data)):
        name_i = name_init(data[i])
        item_i = item_init(data[i])
        items[name_i] = item_i
    _strengthen_arg_list(items)
    return items

# Given an item json, initialize the item object
def item_init(raw_item):
    name = name_init(raw_item)
    try:
        i_type = None
        type_value = raw_item['type']
        for item_type in item.Item_type:
            if type_value == item_type.value:
                i_type = item_type
        if not i_type:
            print("Wrong item type!")
    except KeyError:
        i_type = item.Item_type.NORMAL
    try:
        puzzle_state = raw_item['puzzle_state']
    except KeyError:
        if i_type == item.Item_type.PUZZLE:
            print("Missing puzzle displaying state!")
        puzzle_state = 0
    try:
        raw_states = raw_item['states']
    except KeyError:
        print("Missing item states!")
    if len(raw_states) == 0:
        print("Empty state list!")
    
    states = []
    for i in range(len(raw_states)):
        states.append(state_init(raw_states[i]))
    return item.Item(name=name, states=states, i_type=i_type, puzzle_state=puzzle_state)

# Given a item json, get its name; if not detected, return an empty string
def name_init(raw_item):
    try:
        name = raw_item['name']
    except KeyError:
        print("Missing item name!")
    return name

# Given a state json, initialize the state object
def state_init(raw_state):
    try:
        description = raw_state['description']
    except KeyError:
        print("Missing state description!")
    try:
        label = raw_state['label']
    except KeyError:
        label = ""
    try:
        invisible = raw_state['invisible']
    except KeyError:
        invisible = False
    try:
        dependency_list = raw_state['dependency_list']
    except KeyError:
        dependency_list = []
    try:
        awaken_list = raw_state['awaken_list']
    except KeyError:
        awaken_list = []
    return state.State(description=description, invisible=invisible, label=label, dependency_list=dependency_list, awaken_list=awaken_list)

# Update all the item_name in dependecy_list and awaken_list into the item itself
def _strengthen_arg_list(items):
    for key in items:
        for state in items[key].get_state_list():
            for depend_pair in state.get_dependency_list():
                item_name = depend_pair[0]
                depend_pair[0] = items[item_name]
            awaken_list = state.get_awaken_list()
            for i in range(len(awaken_list)):
                awaken_list[i] = items[awaken_list[i]]

items = system_init(config_file)
print(items)