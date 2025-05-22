# Ollama fills the empty part for the item
import item
import state
import ollama

# Given the item, the current state, the dependencies to the next state, and the next state
# generate a label
def label_generator(item):
    item_name = item.get_name()
    states = item.get_state_list()
    cur_state = states[item.get_state_num()]
    try:
        next_state = states[item.get_state_num() + 1]
    except IndexError:
        print("No further states!")
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
    Example 1:
    If the item is "closet", the current state says "The closet is closed.", and the next state given says "The closet is now open.", you should generate the possible action label "open the closet".
    Example 2:
    If the item is "cup", the current state says "An empty cup", the dependencies say "the tea bag is ready" and "the hot water is ready", and the next state says "A cup of hot tea.", you should generate the possible action label "make tea in the cup".
    Example 3:
    If the item is "painting", the current state says "A painting with a suspicious crease.", and the next state says "A painting with a folded corner, where the secret code is written behind.", you should generate the possible action label "examine the painting".
    """
    user_input = f"""
    Now, the item name is "{item_name}", the current state says "{cur_state.get_description()}"{dependency_text}, and the next state says "{next_state.get_description()}. Now generate a suitable and succinct label for the possible user action."
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
    return response['message']['content']

def room_description_generator(item):
    # Given current room description, and the item's current state
    # generate a new room_description?
    pass

def feedback_generator(item):
    # Given the Pass/Fail, given the current state and the next state
    # generate a feedback
    pass

# ----------------------------------------------------------------- #

# Unit tests
def test_label_generator(item):
    return label_generator(item)

def test_room_description_generator(item):
    pass

def test_feedback_generator(item):
    pass

simple_state_1 = state.State("The bag is closed.")
simple_state_2 = state.State("The bag is now open.")
simple_item = item.Item("bag",[simple_state_1, simple_state_2])

test_label = test_label_generator(simple_item)
print(test_label)

test_room_description = test_room_description_generator(simple_item)
test_feedback = test_feedback_generator(simple_item)