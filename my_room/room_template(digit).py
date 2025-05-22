import item
from item import Item_type
import item_decoder
import item_filler
import action
import puzzle_decoder

def get_input_action_1():
    global items
    while True:
        # Have partly replaced this with LLM action interpreter (engine func2)
        print("Please tell me what are you planning to do now:")
        user_input = input()
        # interpreted = action_interpreter.interpret(user_input)

        nouns = action_interpreter.extract_noun(user_input)
        print(nouns)
        action_interpreter.add_detected_label(nouns, items)
        print(action_interpreter.candidate_labels)
        interpreted = action_interpreter.interpret(user_input)

        if interpreted == 'investigate the painting':
            items[1].interact(items)
            # action_interpreter.add_label('look at the key')
            print(painting.get_feedback(painting.get_state()))
            painting.change_state(1)
            key.change_state(0)
            door.change_state(1)
            return
        elif interpreted == 'unlock the door':
            print(door.get_feedback(door.get_state()))
        elif interpreted == 'ask for clues':
            # default
            # print("There seems to be something on the painting")
            # Feedback generator (ollama)
            print(hint_1(user_input))
        elif interpreted == 'other':
            print("Invalid input. Please try again.")

def get_input_action_2():
    while True:
        # Replace this with LLM action interpreter (engine func2)
        print("Please tell me what are you planning to do now:")
        user_input = input()
        # interpreted = action_interpreter.interpret(user_input)

        nouns = action_interpreter.extract_noun(user_input)
        action_interpreter.add_detected_label(nouns, items)
        interpreted = action_interpreter.interpret(user_input)

        if interpreted == 'look at the painting':
            print(painting.get_feedback(painting.get_state()))
            # action_interpreter.del_label('look at the painting')
        elif interpreted == 'look at the key':
            print(key.get_feedback(key.get_state()))
        elif interpreted == 'unlock the door' or interpreted == 'use the key':
            print(door.get_feedback(door.get_state()))
            # print(key.get_feedback(key.get_state() + 1))
            items[3].interact(items)
            return
        elif interpreted == 'ask for clues':
            # default
            # print("There seems to be something on the painting")
            # Feedback generator (ollama)
            print(hint_2(user_input))
        else:
            print("Invalid input. Please try again.")

# ----------------------------------------------------------------- #

room_description = """
Room Description:\n\n
1. There is a painting nailed to the wall.\n
2. There is a closed door opposite.\n
3. There is a box behind the door.\n
"""

# ----------------------------------------------------------------- #

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
            if item.check_proceeding_status():
                # Successful interact
                if solved:
                    print("Ready to go!")
                    item.proceed_state()
                    print(f"description: {item.get_current_state().get_description()}")
                # Failed interact
                else:
                    print("Incorrect answer!")
                    print(f"description: {item.get_current_state().get_description()}")
            # Failed interact
            else:
                print("Not ready yet (in display state)!")
                print(f"item state num: {item.get_state_num()}; puzzle state: {item.get_puzzle_state_num()}")
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

def input_handler():
    print("Please tell me what are you planning to do now:")
    user_input = input()

    nouns = action_interpreter.extract_noun(user_input)
    labels = action_interpreter.update_labels(nouns, items)
    interpreted = action_interpreter.interpret(user_input, labels)

    valid_input = False
    if interpreted == 'ask for clues':
        valid_input = True
        print("Hint: TODO")
        pass
    else:
        for key in items:
            item = items[key]
            if item.check_invisible():
                continue
            if interpreted == item.get_current_label():
                print(f"Item '{key}' is triggered!")
                interact_with_item(item)
                valid_input = True
                break
    if not valid_input:
        print("(Invalid) Nothing happens.")

item_config_file = "item_config.json"
puzzle_config_file = "puzzle_config.json"
items = item_decoder.system_init(item_config_file)
puzzles = puzzle_decoder.system_init(puzzle_config_file, items)

medium_room = item.Room(items)
action_interpreter = action.Action()

# Mark the end state: last state of "door"

while True:
    input_handler()


# ----------------------------------------------------------------- #


print("-------------------------------------------")
print("Try to Escape!\n")


print(room_description)

get_input_action_1()

print("Room Description:")

print("1. There is a painting nailed to the wall.")
print("2. A key on your hand.")
print("3. There is a closed door opposite.")
print("")

get_input_action_2()

# add the lock

# code behind the painting

# key inside drawer (drawer locked by the lock)

