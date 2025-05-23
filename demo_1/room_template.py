from demo_1.item_old import*
from my_room.action import*

from demo_1.hint_temp import*

def get_input1():
    while True:
        # Replace this with LLM action interpreter (engine func2)
        # With feedback generator (engine func3)
        print("Which one do you want to interact?")
        user_input = int(input())
        if user_input == 1:
            items[1].interact(items)
            print("You find the painting has a tilted corner, and there is a small key sticked to the back of the painting.")
            return
        elif user_input == 2:
            print("You take a closer look at the door, but you have nothing to do with it now.")
        else:
            print("Invalid input. Please try again.")

def get_input2():
    while True:
        # Replace this with LLM action interpreter (engine func2)
        # With feedback generator (engine func3)
        print("Which one do you want to interact?")
        user_input = int(input())
        if user_input == 1:
            print("There is nothing more on the painting now.")
        elif user_input == 2:
            print("A normal key, nothing to look at.")
        elif user_input == 3:
            print("You take a closer look at the door, finding that the keyhole on the door perfectly matches your key.")
            items[3].interact(items)
            return
        else:
            print("Invalid input. Please try again.")

def get_input1_action():
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

        if interpreted == 'look at the painting':
            items[1].interact(items)
            # action_interpreter.add_label('look at the key')
            print("You find the painting has a tilted corner, and there is a small key sticked to the back of the painting.")
            return
        elif interpreted == 'unlock the door':
            print("You take a closer look at the door, but you have nothing to do with it now.")
        elif interpreted == 'ask for clues':
            # TODO: Need feedback generator (engine func3)
            print("There seems to be something on the painting")
        elif interpreted == 'other':
            print("Invalid input. Please try again.")

def get_input2_action():
    while True:
        # Replace this with LLM action interpreter (engine func2)
        print("Please tell me what are you planning to do now:")
        user_input = input()
        # interpreted = action_interpreter.interpret(user_input)

        nouns = action_interpreter.extract_noun(user_input)
        action_interpreter.add_detected_label(nouns, items)
        interpreted = action_interpreter.interpret(user_input)

        if interpreted == 'look at the painting':
            print("There is nothing more on the painting now.")
            # action_interpreter.del_label('look at the painting')
        elif interpreted == 'look at the key':
            print("A normal key, nothing to look at.")
        elif interpreted == 'unlock the door' or interpreted == 'use the key':
            print("You take a closer look at the door, finding that the keyhole on the door perfectly matches your key.")
            items[3].interact(items)
            return
        elif interpreted == 'ask for clues':
            # TODO: Need feedback generator (engine func3)
            print("The lock on the door seems to match the key")
        else:
            print("Invalid input. Please try again.")

# ----------------------------------------------------------------- #

def get_input1_action_2():
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

def get_input2_action_2():
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

painting = Item(1, 'painting', 0, True, False, False, Interactive.INVESTIGATE, 2, None, object_type='INVESTIGATABLE')
key = Item(2, 'key', 0, False, True, False, Interactive.NONE, None, None, object_type='KEY')
door = Item(3, 'door', 0, True, False, True, Interactive.WITH_ITEM, 2, True, object_type='LOCK')

items = [None, painting, key, door]

cur_state = [None, 0, 0, 0]

painting.add_feedback(0, "You find the painting has a tilted corner, and there is a small key sticked to the back of the painting.")
painting.add_feedback(1, "There is nothing more on the painting now.")

key.add_feedback(0, "A normal key, nothing to look at.")
key.add_feedback(1, "You take a closer look at the door, finding that the keyhole on the door perfectly matches your key.")

door.add_feedback(0, "You take a closer look at the door, but you have nothing to do with it now.")
door.add_feedback(1, "You take a closer look at the door, finding that the keyhole on the door perfectly matches your key.")

simple_room = Room(items)
action_interpreter = Action()

print("-------------------------------------------")
print("Try to Escape!")
print("")

# Replace this with 2D/3D Visual Games.
print("Room Description:")

print("1. There is a painting nailed to the wall.")
print("2. There is a closed door opposite.")
print("")

get_input1_action_2()

print("Room Description:")

print("1. There is a painting nailed to the wall.")
print("2. A key on your hand.")
print("3. There is a closed door opposite.")
print("")

get_input2_action_2()