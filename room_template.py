from item import*
from actions import*

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
    while True:
        # Have partly replaced this with LLM action interpreter (engine func2)
        print("Which one do you want to interact?")
        user_input = input()
        interpreted = action_interpreter.interpret(user_input)
        if interpreted == 'see the painting':
            items[1].interact(items)
            action_interpreter.add_label('see the key')
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
        print("Which one do you want to interact?")
        user_input = input()
        interpreted = action_interpreter.interpret(user_input)
        if interpreted == 'see the painting':
            print("There is nothing more on the painting now.")
            action_interpreter.del_label('see the painting')
        elif interpreted == 'see the key':
            print("A normal key, nothing to look at.")
        elif interpreted == 'unlock the door':
            print("You take a closer look at the door, finding that the keyhole on the door perfectly matches your key.")
            items[3].interact(items)
            return
        elif interpreted == 'ask for clues':
            # TODO: Need feedback generator (engine func3)
            print("The lock on the door seems to match the key")
        else:
            print("Invalid input. Please try again.")

painting = Item(1, True, False, False, Interactive.INVESTIGATE, 2, None)
key = Item(2, False, True, False, Interactive.NONE, None, None)
door = Item(3, True, False, True, Interactive.WITH_ITEM, 2, True)

items = [None, painting, key, door]

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

get_input1_action()

print("Room Description:")

print("1. There is a painting nailed to the wall.")
print("2. A key on your hand.")
print("3. There is a closed door opposite.")
print("")

get_input2_action()