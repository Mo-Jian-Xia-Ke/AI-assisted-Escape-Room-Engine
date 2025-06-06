import ollama
from . import item_filler

class HintGenerator:
    def __init__(self, room):
        self.room = room

    # Distribute the hinting task to the correspondent agent
    # General Forward: What to do NEXT?
    # Forward: WHat should we do about xxx?
    # Backward: What to do NOW?
    def hinting_manager(self, user_input):
        pretext = """
        Suppose you are a hinting task manager in an escape room game. Hinting agents are general forward hinting agent, item specific hinting agent, and general backward hinting agent.
        General forward hinting agent select one ready-to-proceed item and hint, suggesting the player what could he immediately do.
        Item speific hinting agent extracts which item the player is asking about, then give a hint to that item. Put '<>' around the item in your output and only output the corresponding item when you decide Item Specific Hinting agent should take the job.
        General backward hinting agent hints about the ultimate goal object, letting the player know what is his goal in a larger scale.
        You will be given the player's request. Your task is to decide which hinting agent to distribute the hinting task to.
        Note: Only output item when distributing the task to "Item Specific Hinting" agent.
        Note: You should output no quotation marks.
        Note: Pay attention to word case in the output.

        Distibuting task Logic:
        [Priviledged] If the player is mentioning or talking about an object, go Item Specific Hinting, together with the item.
        Else if the player is asking what to do next IN GENERAL, go General Forward Hinting.
        Else if the player is asking what to do at the end or what to do to win, go General Backward Hinting.
        """
        # TODO: Dependent Puzzle & Independent Puzzle
        prompt = """
        Here are some examples:
        Example 1:
        Assume the player's request is "What should I do next?".
        Since the player is asking about what to do in general and immediately, the task should be distributed to General Forward Hinting agent.
        So you should output "General Forward Hinting". 
        Example 2:
        Assume the player's request is "What should I do with the painting?".
        Since the player is asking about the "painting", the task should be distributed to Item Specific Hinting agent, and the item "painting" in the item list.
        So you should output "Item Specific Hinting, <painting>". 
        Example 3:
        Assume the player's request is "How to open the box?".
        Since the player is asking about the "box", the task should be distributed to Item Specific Hinting agent, and the item "box" in the item list.
        So you should output "Item Specific Hinting, <box>".
        Example 4:
        Assume the player's request is "What do to with the closet?".
        Since the player is asking about the "closet", the task should be distributed to Item Specific Hinting agent, and the item "closet" in the item list.
        So you should output "Item Specific Hinting, <closet>".
        Example 5:
        Assume the player's request is "What should I do to get out?".
        Since the player is asking about what to do in a larger scope in general, but not what to do immediately, the task should be distributed to General Backward Hinting agent. 
        So you should output "General Backward Hinting". 
        Example 6:
        Assume the player's request is "What should I do to escape?".
        Since the player is asking about what to do in a larger scope in general, but not what to do immediately, the task should be distributed to General Backward Hinting agent. 
        So you should output "General Backward Hinting". 
        """
        input = f"""
        You are now given the information for this task. The player's request is "{user_input}".
        Now decide which agent should take the task and output it.
        """
        posttext = """
        Attention: Do not output your reasonsings. Only output the hinting agent and the potential item in your response. No quotations marks.
        """
        response: ollama.ChatResponse = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': pretext + prompt + input + posttext,
        },
        ])
        raw_response = response['message']['content']

        print(raw_response)
        agent_response = None
        if "Forward" in raw_response:
            agent_response = self.general_forward_hinting()
        elif "Backward" in raw_response:
            agent_response = self.backward_hinting()
        elif "Item" in raw_response:
            start = raw_response.find("<")
            end = raw_response.find(">", start)
            # Feedback error, go to General Foward Hinting
            if start == -1 or end == -1:
                agent_response = self.general_forward_hinting()
            else:
                raw_item = raw_response[start+1:end]
                agent_response = self.item_specific_hinting(raw_item)
        else:
            agent_response = "I'm not sure I fully understand what you mean. Would you mind explaining it a bit more clearly?"
        return agent_response

    # Search all items and select one that all dependcies met
    # Give the hint of the action label
    def general_forward_hinting(self):
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
        input = f"""
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
            'content': pretext + prompt + input + posttext,
        },
        ])
        return response['message']['content']
    
    # Given the hinting item, give the hint of the action label
    # If no such an item or item is invisible, return not found the item
    # If the item can not proceed currently, return cannot proceed now
    # Give the hint of the action label
    def item_specific_hinting(self, raw_item):
        items = self.room.get_items()
        item = None
        for key in items:
            if key in raw_item:
                item = items[key]
                if item.check_invisible():
                    item = None
                    break
                if not item.check_proceeding_status():
                    return "This item doesn't reveal anything new right now. Want to take a look at another one"
                if not item.get_current_label():
                    item.set_current_label(item_filler.label_generator(item))
                label = item.get_current_label()
                break
        if not item:
            return "I'm afraid I couldn't find that item. Could it be a different one? Let me know if there's another item you'd like help with!"
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
        input = f"""
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
            'content': pretext + prompt + input + posttext,
        },
        ])
        return response['message']['content']

    # Find end_item's current state
    # If all dependencies met, give the hint of the action label
    # Else give the hint about the unmet dependencies [Undone]
    # Now, end_item
    # If state invisible, find the object that can awake it?
    def backward_hinting(self):
        end_item = self.room.get_end_item()
        cur_state = end_item.get_current_state()
        next_state = end_item.get_current_state()
        assert next_state, "Should have escaped!"
        if not end_item.get_current_label():
            end_item.set_current_label(item_filler.label_generator(end_item))
        label = end_item.get_current_label()

        if end_item.check_invisible():
            return f"In order to escape, try to find the {end_item}."
        
        pretext = """
        Suppose you are a backward hint generator in an escape room game. You will be given the item's current state, its next state, and the action label for proceeding the state.
        Your task is to hint the player to know the direction of escape on a grand level.
        Note don't provide the extra information in the label and the item's next state. The player should not know them.
        Don't make up extra information by yourself.
        Note better to generate the sentence around the item and mention it explicitly, therefore the user knows which item you are hinting about.
        You can speak in a relatively vague, aiming to hint implicitly.
        """
        prompt = """
        Here are some examples:
        Example 1:
        Assume the item is "closet", the current state says "The closet is closed.", the next state given says "The closet is now open.", and the action label is "open the closet".
        You can hint "In order to get out, the closet is the key."
        Example 3:
        If the item is "door", the current state says "The door is closed", the next state says "The door opens.", and the action label is "open the door".
        You can hint "Think about how to open the door to escape."
        """
        input = f"""
        You are now given the information for this task. The item name is "{end_item.get_name()}", the current state says "{cur_state.get_description()}", the next state says "{next_state.get_description()}, and the action label is "{label}".
        Now generate a hint for the user to know what they should aim to do
        """
        posttext = """
        Attention: Only output the hinting sentence in your response. No quotations marks.
        Note: Do not leak information about the next state and the action label.
        Note: Mention the item.
        """
        response: ollama.ChatResponse = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': pretext + prompt + input + posttext,
        },
        ])
        return response['message']['content']

    def dependent_puzzle_hinting(self):
        pass

    def independent_puzzle_hinting(self):
        pass

# Test
if __name__ == "__main__":
    pass