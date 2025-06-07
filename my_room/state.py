# State proceeding process:
# 1. Check all dependencies (in the current state)
# 2. Go to the next state
# 3. Awake all the items in the awaken_list (of the new state)

# Notice: An invisible state cannot have dependency_list, since they must be awake by others to proceed their state.
# Tip: Check all your invisible items! Make sure they will be awaken by others.
# Notice: The first state (0-th state) of an item cannot have awaken_list, since items are initialized with the first state, such state cannot be proceeded into, thus no awaking call.
# Tip: If you want to awake another item after the first glance of the object, write an additional state with an awaken_list upon the original state!


class State:
    """
    description: for hinting purposes
    dependency_list: a list of tuple pair (item_name, item_state_num)
        where item_num indicates the corresponding item must be in AT LEAST item_state
    awaken_list: a list of items to be notified immediately when the state proceeds to the next state
    room_description: Room description
    """
    def __init__(self, description, invisible=False, label="", dependency_list=[], awaken_list=[], room_description=None):
        self.description = description
        self.invisible = invisible
        self.label = label
        self.dependency_list = dependency_list
        self.awaken_list = awaken_list
        self.room_description = room_description

    def get_description(self):
        return self.description
    
    def get_room_description(self):
        return self.room_description
    
    def set_room_description(self, input):
        self.room_description = input
    
    def check_invisible(self):
        return self.invisible

    def get_dependency_list(self):
        return self.dependency_list
    
    def get_awaken_list(self):
        return self.awaken_list
    
    def get_label(self):
        return self.label
    
    def set_label(self, label):
        self.label = label

    # If no unmet dependencies, return True; else return False
    def check_proceeding_status(self):
        return not self.search_unmet_dependency()

    # Return a list of all unmet dependencies
    def search_unmet_dependency(self):
        unmet_dep = []
        for depend_pair in self.dependency_list:
            item = depend_pair[0]
            item_state_num = depend_pair[1]
            if item.get_state_num() < item_state_num:
                unmet_dep.append(item)
        return unmet_dep
        
    # Awake the following items, let their state + 1 immediately
    def awake_all(self):
        for item in self.awaken_list:
            item.proceed_state()
        
                
