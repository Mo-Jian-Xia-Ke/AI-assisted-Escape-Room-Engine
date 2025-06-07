import sys
from .item import ItemType
from . import auto_generator, item_decoder, action, puzzle_decoder, room, hint_generator

# Display room descriptions. If empty, generate them.
def display_room_description(room):
    item_counter = 1
    room_description = "\nRoom Description: \n"
    items = room.get_items()
    for key in items:
        item = items[key]
        if item.check_invisible():
            continue
        if not item.get_room_description():
            item.set_room_description(auto_generator.room_description_generator(item))
        room_description += f"{item_counter}: {item.get_room_description()}\n"
        item_counter += 1
    print(room_description)

def interact_with_item(room, item, user_input):
    if item.check_end_state():
        status = 'failure'
        status_detail = 'end state'
    elif 'invalid' in room.get_action_interpreter().valid_interaction_check(item):
        print("Validation: " + room.get_action_interpreter().valid_interaction_check(item))
        status = 'failure'
        status_detail = 'invalid move'
    elif item.get_type() == ItemType.PUZZLE and item.check_display_status():
        solved = item.display_puzzle()
        if item.check_proceeding_status():
            if solved:
                if item.check_proceeding_status():
                    if item.check_code_status():
                        status = 'success'
                        status_detail = 'normal'
                    else:
                        status = 'success'
                        status_detail = 'lack code'
            else:
                status = 'failure'
                status_detail = 'incorrect code'
        else:
            status = 'failure'
            status_detail = 'guarded'
    else:
        # Normal Situations
        if item.check_proceeding_status():
            status = 'success'
            status_detail = 'normal'
        else:
            status = 'failure'
            status_detail = 'guarded'

    print(f"status: {status}, status_detail: {status_detail}")
    print(auto_generator.feedback_generator(status=status, status_detail=status_detail, input=user_input, item=item))
    if status == 'success':
        item.proceed_state()

def input_handler(room):
    end_game = False

    display_room_description(room)

    print("Please tell me what are you planning to do now:")
    print(">", end="")
    user_input = input()
    # Avoid empty input
    if user_input == "":
        user_input = "."
    if user_input == "quit":
        sys.exit()

    # nouns = room.get_action_interpreter().extract_noun(user_input)
    # labels = room.get_action_interpreter().update_labels(nouns, room.get_items())
    # interpreted = room.get_action_interpreter().interpret(user_input, labels)

    interpreted_label = room.get_action_interpreter().interpret(user_input)

    valid_input = False
    if interpreted_label == 'ask for hint':
        valid_input = True
        hints = room.get_hint_generator().hinting_manager(user_input)
        print(hints)
    else:
        for key in room.get_items():
            item = room.get_items()[key]
            if item.check_invisible():
                continue
            if interpreted_label == item.get_current_label():
                print(f"Item '{key}' is triggered!")
                interact_with_item(room, item, user_input)
                valid_input = True
                if room.check_end_state():
                    end_game = True
                break
    if not valid_input:
        print(auto_generator.feedback_generator(status='failure', status_detail='no item', input=user_input))
    
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

    action_interpreter = action.Action(items, "hybrid")
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