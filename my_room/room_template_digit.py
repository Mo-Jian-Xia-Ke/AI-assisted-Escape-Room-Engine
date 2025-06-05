import sys
from .item import ItemType
from . import item_decoder, item_filler, action, puzzle_decoder, room, hint_generator

# [Temp] room description
def display_room_description(room):
    item_counter = 1
    room_description = "\nRoom Description: \n"
    items = room.get_items()
    for key in items:
        item = items[key]
        if item.check_invisible():
            continue
        room_description += f"{item_counter}: {item.get_current_state().get_description()}\n"
        item_counter += 1
    print(room_description)

# [Temp] feedbacks
def feedback_success(item):
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("Ready to go!")
    item.proceed_state()
    print(f"New description: {item.get_current_state().get_description()}")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

# [Temp] feedbacks
def feedback_failure(item):
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("Not ready yet!")
    if item.get_type() == ItemType.PUZZLE:
        print(f"item state num: {item.get_state_num()}; puzzle state: {item.get_puzzle_state_num()}")
    print(f"Current description(still): {item.get_current_state().get_description()}")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

def interact_with_item(item):
    # Failed interact (end state)
    if item.check_end_state():
        print(f"End state for {item.get_name()}!")
        return

    if item.get_type() == ItemType.NORMAL:
        # Successful interact
        if item.check_proceeding_status():
           feedback_success(item)
        # Failed interact
        else:
            feedback_failure(item)

    elif item.get_type() == ItemType.PUZZLE:
        if item.check_display_status():
            solved = item.display_puzzle()
            if solved:
                # Successful interact
                if item.check_proceeding_status():
                    feedback_success(item)
                # Failed interact
                else:
                    feedback_failure(item)
            # Failed interact (Ver 2)
            else:
                print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
                print("Incorrect answer!")
                print(f"Current description(still): {item.get_current_state().get_description()}")
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        # Successful interact
        elif item.check_proceeding_status():
            feedback_success(item)
        # Failed interact
        else:
            feedback_failure(item)

def input_handler(room):
    end_game = False

    display_room_description(room)

    print("Please tell me what are you planning to do now:")
    user_input = input()
    # Avoid empty input
    if user_input == "":
        user_input = "."
    if user_input == "quit":
        sys.exit()

    nouns = room.get_action_interpreter().extract_noun(user_input)
    labels = room.get_action_interpreter().update_labels(nouns, room.get_items())
    interpreted = room.get_action_interpreter().interpret(user_input, labels)

    valid_input = False
    if interpreted == 'ask for hint':
        valid_input = True
        hints = room.get_hint_generator().hinting_manager(user_input)
        print(hints)
    else:
        for key in room.get_items():
            item = room.get_items()[key]
            if item.check_invisible():
                continue
            if interpreted == item.get_current_label():
                print(f"Item '{key}' is triggered!")
                interact_with_item(item)
                valid_input = True
                if room.check_end_state():
                    end_game = True
                break
    if not valid_input:
        print("(Invalid) Nothing happens.")
    
    if end_game:
        print("Success! Game ends now...")
        return True
    return False

# Game starts
def main():
    # [For Developers to modify]
    item_config_file = "my_room/item_config.json"
    puzzle_config_file = "my_room/puzzle_config.json"
    items = item_decoder.system_init(item_config_file)
    puzzles = puzzle_decoder.system_init(puzzle_config_file, items)
    end_item = items['door']
    end_state = end_item.get_state_list()[-1]

    action_interpreter = action.Action()
    medium_room = room.Room(items, puzzles, action_interpreter, end_item, end_state)
    hint_system = hint_generator.HintGenerator(medium_room)
    medium_room.set_hint_generator(hint_system)

    # If the game has not reached the end state, keep continue the input-action loop
    end_game = False
    while not end_game:
        end_game = input_handler(medium_room)

    print("Congrat!!!!!")

if __name__ == "__main__":
    main()