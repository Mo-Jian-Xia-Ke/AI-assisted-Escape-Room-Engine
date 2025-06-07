# Ollama fills the empty part for the item
import ollama
from . import item, state

# Given the item, the current state, the dependencies to the next state, and the next state
# generate a label
def label_generator(item):
    # Not consistent enough!
    item_name = item.get_name()
    cur_state = item.get_current_state()
    next_state = item.get_next_state()
    dependencies = cur_state.get_dependency_list()

    dependency_text = ""
    if dependencies:
        description_list = "["
        for depend_pair in dependencies:
            depend_item = depend_pair[0]
            depend_state_num = depend_pair[1]
            depend_state = depend_item.get_state_list()[depend_state_num]
            description_list += f"\"{depend_state.get_description()}\", "
        description_list = description_list[:-2] + ']'
        dependency_text = f", the dependencies say {dependency_text}"

    pretext = """
    Suppose you are a label generator in an escape room game. Label refers the most possible action that can proceed from the current state to the next state.
    Your task is to provide suitable and succinct label for the NLP model to fit on user's action.
    """
    prompt = """
    Here are some examples:
    Example 1:
    If the item is "closet", the current state says "The closet is closed.", and the next state given says "The closet is now open.", you should generate the possible action label "open the closet".
    Example 2:
    If the item is "cup", the current state says "An empty cup", the dependencies say "the tea bag is ready" and "the hot water is ready", and the next state says "A cup of hot tea.", you should generate the possible action label "make tea in the cup".
    Example 3:
    If the item is "painting", the current state says "A painting with a suspicious crease.", and the next state says "A painting with a folded corner, where the secret code is written behind.", you should generate the possible action label "examine the painting".
    Example 4:
    If the item is "lock", the current state says "A normal digital lock.", and the next state given says "The lock is unlocked.", you should generate the possible action label "try the lock".
    """
    user_input = f"""
    Now, the item name is "{item_name}", the current state says "{cur_state.get_description()}"{dependency_text}, and the next state says "{next_state.get_description()}. Now generate a suitable, general and succinct label for the possible user action."
    """
    posttext = """
    Notice: Converge the action to only one branch, without using 'or' to connect long actions.
    Attention: Only output the label in your response. No punctuations.
    """
    response: ollama.ChatResponse = ollama.chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': pretext + prompt + user_input + posttext,
    },
    ])
    return response['message']['content'].strip('\'".').lower()

def room_description_generator(item):
    # Given current room description, and the item's current state
    # generate a new room_description?
    pretext = """
    Suppose you are a room description generator in an escape room game.
    Given the item name and the designer's description, your task is to generate a suitable description of the given item to display it to the player.
    """
    prompt = """
    Here are some examples:
    Example 1:
    If the item is "door", the designer's description is "A closed door.".
    You can generate "There is a closed door in the room."
    Example 2:
    If the item is "door", the designer's description is "A locked box.".
    You can generate "A locked box on the ground."
    Example 3:
    If the item is "painting", the designer's description is "A painting with a folded corner. Code '9827' written behind.".
    You can generate "A painting with a folded corner, where a series of numbers '9827' is written behind."
    Example 4:
    If the item is "handle", the designer's description is "An assemblable door handle."
    You can generate "A delicate door handle that looks like it could be mounted on a door."
    """
    user_input = f"""
    Now, the item name is "{item.get_name()}", the developer's description is "{item.get_description()}".
    """
    posttext = """
    Note: Keep sentences short. Don't over deduct.
    Attention: Only generate sentences, no quotation marks.
    Attention: ONLY output the description.
    """
    response: ollama.GenerateResponse = ollama.generate(model='llama3.2', prompt=pretext + prompt + user_input + posttext)
    return response['response']

# Given the detailed Pass/Fail, given the user input, the current state and the next state
# generate a feedback
# Success status details: ['normal', 'lack code']
# Failure status details: ['no item', 'invalid move', 'guarded', 'end state', 'incorrect code']
def feedback_generator(status, status_detail, input, item=None):
    if status == 'failure' and status_detail == 'no item':
        return "Hmm, I'm not certain what you're referring to. Can you explain it a bit more clearly?"

    assert item, "Error: Missing feedback item!"
    next_state_text = ""
    if status == 'success':
        assert not item.check_end_state(), "Error: End state!"
        next_state_text = f", and the next state's description is \"{item.get_next_state().get_description()}\""

    pretext = """
    Suppose you are a feedback generator in an escape room game.
    Given the player's input, the item's current state and maybe the next state, your task is to provide feedback regarding to the player's action.
    """
    if status == 'success':
        detailed_prompt = _success_feedback(status_detail)
    else:
        detailed_prompt = _failure_feedback(status_detail)

    user_input = f"""
    Now, the player's input is "{input}", the item's current state's description is "{item.get_description()}"{next_state_text}.
    Provide your feedback.
    """
    posttext = """
    Note: Keep sentences short. Don't over deduct.
    Attention: Only generate sentences, no quotation marks.
    Attention: ONLY output the feedback.
    """
    response: ollama.GenerateResponse = ollama.generate(model='llama3.2', prompt=pretext + detailed_prompt + user_input + posttext)
    return "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\nFeedback: " + response['response'] + "\nvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n"

def _success_feedback(status_detail):
    if status_detail == 'lack code':
        prompt = """
        The situation now is the player has input the correct code of the puzzle, yet before getting the code information.
        It means that the player should not have the enough information to solve the puzzle, but he luckily did.

        For feedback, here are some examples:
        Example 1:
        If the player's input is "I want to open the lock", the item's current state's description is "A normal padlock that locks the box.", and the next state's description is "An unlocked lock on the box."
        You can provide the feedback: "You hear a click. The lock opens... but you can't help but wonder: how did you know the code?"

        Example 2:
        If the player's input is "I want to examine the lock", the item's current state's description is "A normal digital lock on the box that protects it.", and the next state's description is "An unlocked lock on the box."
        You can provide the feedback: "It worked? Strange... the code matched — but you haven't seen it anywhere yet."

        Example 3:
        If the player's input is "I want to examine the clock", the item's current state's description is "A clock with movable hands", and the next state's description is "A clock showing 5:30, with the cabinet door below it now open."
        You can provide the feedback: "You just fiddled with the hands on the clock and the cupboard opened, how weird?!"
        """
    else:
        # status_detail: normal
        prompt = """
        The situation now is the player's action successfully take him to the item's next state.
        The feedback should fit the player's input, and perform as the action that makes current state flows reasonably to the next state.

        For feedback, here are some examples:
        Example 1:
        If the player's input is "I want to examine the painting", the item's current state's description is "A painting with a suspicious crease.", and the next state's description is "A painting with a folded corner, with '0619' written behind."
        You can provide the feedback: "You revealed a corner of the painting."

        Example 2:
        If the player's input is "I want to open the box", the item's current state's description is "A closed box.", and the next state's description is "An open box with a handle inside."
        You can provide the feedback: "You opened the box, and found a handle laying inside."

        Example 3:
        If the player's input is "I want to examine the box", the item's current state's description is "A closed box.", and the next state's description is "An locked box."
        You can provide the feedback: "You checked the box and found it was locked."

        Example 4:
        If the player's input is "I want to open the lock", the item's current state's description is "A normal digital lock on the box that protects it.", and the next state's description is "An unlocked lock on the box."
        You can provide the feedback: "You have successfully unlocked the lock!"
        """
    return prompt

def _failure_feedback(status_detail):
    if status_detail == 'end state':
        prompt = """
        The situation now is the player's intends to interact with an item at its end state.
        Since the item is in the end state, the item can provide no further clues or new feedback.

        For feedback, here are some examples:
        Example 1:
        If the player's input is "I want to examine the painting", the item's current state's description is "A painting with a folded corner, with '0619' written behind."
        You can provide the feedback: "You've already examined this painting thoroughly."

        Example 2:
        If the player's input is "I want to open the box", the item's current state's description is "An open closet."
        You can provide the feedback: "You feel like the closet has revealed all it can."

        Example 3:
        If the player's input is "I want to examine the box", the item's current state's description is "An empty box."
        You can provide the feedback: "It's empty. Maybe it's time to look elsewhere."

        Example 4:
        If the player's input is "I want to open the lock", the item's current state's description is "An unlocked lock on the box."
        You can provide the feedback: "The lock has already been opened."
        """
    elif status_detail == 'guarded':
        prompt = """
        The situation now is the player's intends to interact with an item, but there are some preparations have been done or its dependencies have been met totally, so the interaction failed at this moment.
        The feedback should indicates that this item is not ready to be interactted currently.

        For feedback, here are some examples:
        Example 1:
        If the player's input is "I want to use the cup", the item's current state's description is "An empty cup on the table."
        You can provide the feedback: "You see a cup, but there's nothing inside and nothing to do with it... yet."

        Example 2:
        If the player's input is "I want to try open the door", the item's current state's description is "A closed door."
        You can provide the feedback: "The door is firmly shut."

        Example 3:
        If the player's input is "I want to open the box", the item's current state's description is "A locked box."
        You can provide the feedback: "The box is locked and won't open for now."

        Example 4:
        If the player's input is "I want to examine the lock", the item's current state's description is "A normal lock that protects the box."
        You can provide the feedback: "You try, but nothing you have fits the lock."
        """
    elif status_detail == 'incorrect code':
        prompt = """
        The situation now is the player's has input the wrong code to the puzzle.

        For feedback, here are some examples:
        Example 1:
        If the player's input is "I want to open the lock", the item's current state's description is "A digital lock that protects the suitcase."
        You can provide the feedback: "Wrong code. Try again."

        Example 2:
        If the player's input is "I want to examine the lock", the item's current state's description is "A padlock on the box."
        You can provide the feedback: "Nothing happens."

        Example 3:
        If the player's input is "I want to examine the clock", the item's current state's description is "A clock with movable hands."
        You can provide the feedback: "You try adjusting it, but the clock remains still."
        """
    else:
        # status_detail: invalid move
        prompt = """
        The situation now is the player's intends to interact with an item, but not in the right way.
        It could be not correctly interactting with the item or just some abnormal, imaginative actions.

        For feedback, here are some examples:
        Example 1:
        If the player's input is "I want to tear up the painting.", the item's current state's description is "A painting with a suspicious crease."
        You can provide the feedback: "Now may not be the best time to ruin a potential clue."

        Example 2:
        If the player's input is "I want to force the lock open", the item's current state's description is "A digital lock that protects the box."
        You can provide the feedback: "The lock is specially reinforced --- there's no way to pry it open."

        Example 3:
        If the player's input is "Punch the door with all my strength", the item's current state's description is "A closed door."
        You can provide the feedback: "Your hand hurts. The door doesn't budge. You start to feel a little foolish."

        Example 4:
        If the player's input is "Pour the water in the cup over myself.", the item's current state's description is "A cup filled with water."
        You can provide the feedback: "The cup of water seems to protest being wasted like that."
        """
    return prompt

# ----------------------------------------------------------------- #

# Unit tests
def test_label_generator(item):
    return label_generator(item)

def test_room_description_generator(item):
    pass

def test_feedback_generator(item):
    pass

if __name__ == "__main__":
    simple_state_1 = state.State("The bag is closed.")
    simple_state_2 = state.State("The bag is now open.")
    simple_item = item.Item("bag",[simple_state_1, simple_state_2])

    test_label = test_label_generator(simple_item)
    print(test_label)

    test_room_description = test_room_description_generator(simple_item)
    test_feedback = test_feedback_generator(simple_item)