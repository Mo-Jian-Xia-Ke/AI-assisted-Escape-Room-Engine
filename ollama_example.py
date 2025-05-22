import ollama
from ollama import chat
from ollama import ChatResponse

# response: ChatResponse = chat(model='llama3.2', messages=[
#   {
#     'role': 'user',
#     'content': '1+1 = ?',
#   },
# ])
# print(response['message']['content'])
# # or access fields directly from the response object
# print(response.message.content)

# ollama.generate(model='llama3.2', prompt='Why is the sky blue?')
# print(ollama.response)

# Chat is Stateful, while Generate is Stateless

# --- #
pretext = """
Suppose you are the hint generating agent in an escape room game.
Your task is to provide the hint given the following information,
including the room description, the correct action that shoule be interacted on a speific object, and the possible feedback after the correct interaction.
"""
posttext = """
You need to deduct from the feedback after the correct action to find the detail of that action, and hint the player to do the correct action.
Now, you should provide you hint based on the information above.
Notice: The information regarding the "Correct action" and the "Feedback after that action" are not known by the player. you should implicitly imply the player to take that action, but not directly notice him the potential feedback of that action.
Notice: Do not over-deduct what will happen next in the game.
Notice: Do not add any non-existing detail out of the "Room Description".
Attention: Only produce the feedback to the user in your response.
"""

def hint_1(user_input):
    room_description = """
    Room Description:
    1. There is a painting nailed to the wall.
    2. There is a closed door opposite.   
    """
    next_label = "Correct action: investigate the painting"
    next_feedback = "Feedback after that action: You find the painting has a tilted corner, and there is a small key sticked to the back of the painting."
    user_text = "Now the player inputs:\"" + user_input
    response: ChatResponse = chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': pretext + room_description + next_label + next_feedback + user_text + posttext,
    },
    ])
    return response['message']['content']

def hint_2(user_input):
    room_description = """
    Room Description:
    1. There is a painting nailed to the wall.
    2. A key on your hand.
    3. There is a closed door opposite.
    """
    next_label = "Correct action: use the key, unlock the door"
    next_feedback = "Feedback after that action: You take a closer look at the door, finding that the keyhole on the door perfectly matches your key. Then you escape."
    user_text = "Now the player inputs:\"" + user_input
    response: ChatResponse = chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': pretext + room_description + next_label + next_feedback + user_text + posttext,
    },
    ])
    return response['message']['content']

# ollama.pull('llama3.2')
print(hint_1("What should I do now?"))

# Not stable
# Sometimes overhinting (e.g. The key is on the back)
#   -> to add more constriants
# Sometimes non-sense hinting (e.g. You've unlocked the door, but you're still on the other side. The room is dimly lit, and you hear a faint noise coming from the hallway. You need to focus on finding a way out. What's next?)
#   -> consider better prompting? 

# e.g.
# {"role": "system", "content": "You are a concise and helpful in-game hint master. Only respond with actionable hints. Do not give solutions."}
