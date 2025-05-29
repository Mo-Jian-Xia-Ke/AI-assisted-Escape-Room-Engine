import ollama
from . import item_filler

class HintGenerator:
    def __init__(self, room):
        self.room = room

    # TODO: Let LLM decide which agent to call
    def hinting_manager(self, user_input):
        hint_1 = self.forward_hinting()
        hint_2 = self.backward_hinting()
        print(f"Hint 1: {hint_1}")
        print(f"Hint 2: {hint_2}")

    # Search all items and select one that all dependcies met
    # Give the hint of the action label
    def forward_hinting(self):
        items = self.room.get_items()
        item = None
        for key in items:
            item = items[key]
            if item.check_invisible() or not item.check_proceeding_status():
                continue
            if not item.get_current_label():
                item.set_current_label(item_filler.label_generator(item))
            label = item.get_current_label()
            break
        cur_state = item.get_current_state()
        next_state = item.get_next_state()

        pretext = """
        Suppose you are a forward hint generator in an escape room game. You will be given the item's current state, its next state, and the action label for proceeding the state.
        Your task is to hint the player to take the action that can be interpreted quite similar to the given action label.
        Note don't provide the extra information in the label and the item's next state. The player should not know them.
        Don't make up extra information by yourself.
        Note better to generate the sentence around the item and mention it explicitly, therefore the user knows which item you are hinting about.
        You can speak in a relatively relax tone, as a human providing hints.
        """
        prompt = """
        Here are some examples:
        Example 1:
        Assume the item is "closet", the current state says "The closet is closed.", the next state given says "The closet is now open.", and the action label is "open the closet".
        You can hint "What about try the closet?"
        Example 2:
        If the item is "cup", the current state says "An empty cup", the next state says "A cup of hot tea.", and the action label is "make tea in the cup".
        You can hint "Brew yourself a cup of tea and unwind."
        Example 3:
        If the item is "painting", the current state says "A painting with a suspicious crease.", the next state says "A painting with a folded corner, where the secret code is written behind.", and the action label is "examine the painting".
        You can hint "The painting seems weird. Take a closer look."
        """
        # 1. " If this were a horror game, this is where the jump scare would be. Good thing it's not… or is it?"
        # 3. "Even the most innocent artwork can conceal a secret. What might lie beneath the fold?"
        user_input = f"""
        You are now given the information for this task. The item name is "{item.get_name()}", the current state says "{cur_state.get_description()}", the next state says "{next_state.get_description()}, and the action label is "{label}".
        Now generate a hint for the user to get to the next state.
        """
        posttext = """
        Attention: Only output the hinting sentence in your response. No quotations marks.
        Note: Do not leak information about the next state and the action label.
        Note: Mention the item.
        """
        response: ollama.ChatResponse = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': pretext + prompt + user_input + posttext,
        },
        ])
        return response['message']['content']
    
    # Find end_state, backtrack to that item's current state
    # If all dependencies met, give the hint of the action label
    # Else give the hint about the unmet dependencies
    # If state invisible, find the object that can awake it?
    def backward_hinting(self):
        return "On the way!"
        pass

    def dependent_puzzle_hinting(self):
        pass

    def independent_puzzle_hinting(self):
        pass

# Test
if __name__ == "__main__":
    pass