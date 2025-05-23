import item
from item import Item_type
import item_decoder
import item_filler
import action
import puzzle_decoder
import room

# Temp room description
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

def interact_with_item(item):
    # Failed interact (end state)
    if item.check_end_state():
        print(f"End state for {item.get_name()}!")
        return

    if item.get_type() == Item_type.NORMAL:
        # Successful interact
        if item.check_proceeding_status():
            print("Ready to go!")
            item.proceed_state()
            print(f"description: {item.get_current_state().get_description()}")
        # Failed interact
        else:
            print("Not ready yet!")
            print(f"description: {item.get_current_state().get_description()}")

    elif item.get_type() == Item_type.PUZZLE:
        if item.check_display_status():
            solved = item.display_puzzle()
            if solved:
                # Successful interact
                if item.check_proceeding_status():
                    print("Ready to go!")
                    item.proceed_state()
                    print(f"description: {item.get_current_state().get_description()}")
                # Failed interact
                else:
                    print("Not ready yet (in display state)!")
                    print(f"item state num: {item.get_state_num()}; puzzle state: {item.get_puzzle_state_num()}")
                    print(f"description: {item.get_current_state().get_description()}")
            # Failed interact
            else:
                print("Incorrect answer!")
                print(f"description: {item.get_current_state().get_description()}")
        # Successful interact
        elif item.check_proceeding_status():
            print("Ready to go!")
            item.proceed_state()
            print(f"description: {item.get_current_state().get_description()}")
        # Failed interact
        else:
            print("Not ready yet!")
            print(f"item state num: {item.get_state_num()}; puzzle state: {item.get_puzzle_state_num()}")
            print(f"description: {item.get_current_state().get_description()}")   

def input_handler(room):
    end_game = False

    display_room_description(room)

    print("Please tell me what are you planning to do now:")
    user_input = input()
    # Avoid empty input
    if user_input == "":
        user_input = "."

    nouns = action_interpreter.extract_noun(user_input)
    labels = action_interpreter.update_labels(nouns, room.get_items())
    interpreted = action_interpreter.interpret(user_input, labels)

    valid_input = False
    if interpreted == 'ask for clues':
        valid_input = True
        print("Hint: TODO")
        pass
    else:
        for key in room.get_items():
            item = room.get_items()[key]
            if item.check_invisible():
                continue
            if interpreted == item.get_current_label():
                print(f"Item '{key}' is triggered!")
                interact_with_item(item)
                valid_input = True
                if room.check_end_state(item.get_current_state()):
                    end_game = True
                break
    if not valid_input:
        print("(Invalid) Nothing happens.")
    
    if end_game:
        print("Success! Game ends now...")
        return True
    return False

# Game starts
if __name__ == "__main__":
    item_config_file = "item_config.json"
    puzzle_config_file = "puzzle_config.json"
    items = item_decoder.system_init(item_config_file)
    puzzles = puzzle_decoder.system_init(puzzle_config_file, items)
    end_state = items['door'].get_state_list()[-1]

    medium_room = room.Room(items, puzzles, end_state)
    action_interpreter = action.Action()

    # If the game has not reached the end state, keep continue the input-action loop
    end_game = False
    while not end_game:
        end_game = input_handler(medium_room)

    print("Congrat!!!!!")