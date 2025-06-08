# http://huggingface.co/facebook/bart-large-mnli

import transformers

import spacy
import en_core_web_sm

import nltk
from nltk.corpus import wordnet

import ollama

from . import auto_generator, state, item

# classifier usage example:
# sequence_to_classify = "What should I do now?"
# candidate_labels = ['ask for clues', 'open the lock', 'open the drawer', 'look at the drawer']
# result = classifier(sequence_to_classify, candidate_labels)

# result examples:
# {'sequence': 'I want to use the key to open the door', 'labels': ['open the lock', 'ask for clues', 'move the table'], 'scores': [0.9374002814292908, 0.04698718339204788, 0.015612520277500153]}
# {'sequence': 'I want to check the drawer', 'labels': ['look at the drawer', 'open the drawer', 'ask for clues', 'open the lock'], 'scores': [0.6368684768676758, 0.33628571033477783, 0.018994150683283806, 0.007851657457649708]}
# {'sequence': 'What should I do now?', 'labels': ['ask for clues', 'open the lock', 'open the drawer', 'look at the drawer'], 'scores': [0.8905602693557739, 0.05941273644566536, 0.028227612376213074, 0.021799379959702492]}

class Action:
    def __init__(self, items, mode="hybrid", acceptance_threshold = 0.75):
        nltk.download('wordnet', quiet=True)
        self.items = items
        self.mode = mode
        self.acceptance_shreshold = acceptance_threshold
        self.candidate_labels = ['ask for hint', 'other']
        self.classifier = transformers.pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.input = ""
    
    def interpret(self, new_input):
        self.input = new_input
        labels = self.update_all_labels()
        print("Labels: ", end = "")
        print(labels)
        if self.mode == "nlp":
            return self.nlp_mode(labels)
        elif self.mode == "llm":
            return self.llm_mode(labels)
        else:
            return self.hybrid_mode(labels)
        
    def nlp_mode(self, labels):
        print("NLP mode:")
        if '?' in self.input or 'hint' in self.input:
            return 'ask for hint'
        noun = self.extract_main_noun()
        print(noun)
        if not noun:
            return 'other'
        item_name = self.match_by_synonym(noun)
        if not item_name:
            return 'other'
        return self.items.get(item_name).get_current_label()
            
    def llm_mode(self, labels):
        label, _ = self.bart_interpret(labels)
        print("LLM mode:")
        return label

    def hybrid_mode(self, labels):
        print("Hybrid mode:")
        label = self.nlp_mode(labels)
        if label == 'ask for hint' or label == 'other':
            label = self.llm_mode(labels)
        return label
        
    # Check whether the user's action is valid to proceed the item's state
    # used to check to give succesful/failed feedback
    def valid_interaction_check(self, item):
        pretext = """
        Suppose you are a interaction validator in an escape room game.
        Given the player's input, the item name, the item's current state and the next state, your task is to determine whether the player's input is reasonable to make the item proceed to the next state.
        """
        prompt = """
        Here are some examples:
        Example 1:
        If the item is "painting", the player inputs "I want to examine the painting", the current state is "A painting with a suspicious crease.", the next state is "A painting with a folded corner, with '0619' written behind.".
        It seems a correspondent move, so you should respond "valid".
        Example 2:
        If the item is "painting", the player inputs "Burn the painting", the current state is "A painting with a suspicious crease.", the next state is "A painting with a folded corner, with '0619' written behind.".
        It is too violent and can not lead to the next state, so you should respond "invalid".
        Example 3:
        If the item is "box", the player inputs "Open the box.", the current state is "A closed box with a lock.", the next state is "An open box with a golden key inside".
        It seems a correspondent move, so you should respond "valid".
        Example 4:
        If the item is "box", the player inputs "I want to throw the box to the ground.", the current state is "A closed box with a lock.", the next state is "An open box with a golden key inside".
        It is not the right way to open the box since it has a lock outside, so you should respond "invalid".
        Example 5:
        If the item is "lock", the player inputs "I want to examine the lock.", the current state is "A normal digital lock", the next state is "The lock is open now.".
        It seems the right move, so you should respond "valid".
        Example 6:
        If the item is "lock", the player inputs "I want to pry the lock.", the current state is "A normal digital lock", the next state is "The lock is open now.".
        The digital lock puzzle is not designed to be pryed, so you should respond "invalid".
        """
        user_input = f"""
        Now, the item is "{item.get_name()}", the player inputs "{self.input}", the current state is "{item.get_description()}", and the next state is "{item.get_next_state().get_description()}".
        """
        posttext = """
        Attention: Only output the word "valid" or "invalid". No codes or reasoning steps.
        """
        response: ollama.GenerateResponse = ollama.generate(model='llama3.2', prompt=pretext + prompt + user_input + posttext)
        return response['response'].strip('\'".').lower()

    # ---------- Label update function ---------- #
    
    def update_all_labels(self):
        # A shallow copy of the list by slicing
        added_labels = self.candidate_labels[:]
        for key in self.items:
            item = self.items[key]
            # If item is invisible now, skip this item.
            if item.check_invisible():
                continue
            # Deal with end state label for feedback
            if not item.get_current_label():
                if item.check_end_state():
                    item.set_current_label(f"interact with the {item.get_name()}")
                else:
                    item.set_current_label(auto_generator.label_generator(item))
            added_labels.append(item.get_current_label())
        return added_labels

    # ---------- NLP interpreters ---------- #
    
    # Try to extract the main component noun of the sentence
    def extract_main_noun(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.input)
        # extent the object first (dobj / pobj / obj)
        for token in doc:
            if token.dep_ in ("dobj", "pobj", "obj") and token.pos_ == "NOUN":
                return token.text
        # Then the subject (nsubj)
        for token in doc:
            if token.dep_ in ("nsubj",) and token.pos_ == "NOUN":
                return token.text
        # fallback：the first noun
        for token in doc:
            if token.pos_ == "NOUN":
                return token.text
        return None
    
    # use wordnet to generate a synonym list
    def get_wordnet_synonyms(self, word):
        synonyms = set()
        for synset in wordnet.synsets(word, pos=wordnet.NOUN):  # Focus on nouns
            for lemma in synset.lemmas():
                synonyms.add(lemma.name().replace('_', ' ').lower())
        return list(synonyms)
    
    # Synonyms:
    # painting: {'painting', 'house painting', 'picture'}
    # box: {'box seat', 'box', 'corner', 'boxful', 'boxwood', 'loge'}
    # handle: {'grip', 'hold', 'handle', 'handgrip'}
    # lock: {'whorl', 'curl', 'lock chamber', 'ignition lock', 'lock', 'ringlet'}
    # door: {'room access', 'door', 'doorway', 'threshold'}
    
    # match synonyms
    def match_by_synonym(self, user_word):
        user_synonyms = set(self.get_wordnet_synonyms(user_word))
        for item_name in self.items:
            item_synonyms = set(self.get_wordnet_synonyms(item_name))
            if user_word == item_name or user_word in item_synonyms or item_name in user_synonyms:
                return item_name  # matched item
        return None
    
    # ---------- LLM interpreters ---------- #

    # Return the label with the highest correspondent score and that score
    def bart_interpret(self, labels):
        results = self.classifier(self.input, labels)
        print()
        print("Results: ", end = "")
        print(results)
        print()
        label = results['labels'][0]
        score = results['scores'][0]
        return (label, score)  

# ----------------------------------------------------------------- #

# Unit tests
# def item_extaction_test():
#     # LLM error too much!
#     box_state_1 = state.State("The box is closed.")
#     box_state_2 = state.State("The box is now open.")
#     box = item.Item("box", [box_state_1, box_state_2])
#     painting_state_1 = state.State("The painting is on the wall.")
#     painting_state_2 = state.State("The painting has been pulled to the ground.")
#     painting = item.Item("painting", [painting_state_1, painting_state_2])
#     door_state_1 = state.State("The door is shut forever.")
#     door = item.Item("door", [door_state_1])
#     items = {"box": box, "painting": painting, "door": door}
#     input1 = "I want to open the box."
#     input2 = "I want to break that case."
#     input3 = "Take a closer look at the painting."
#     input4 = "I want to tear the drawing apart."
#     input5 = "I want to examine the floor."
#     input6 = "I want to ignite the candle."
#     action_interpreter = Action(items, "llm")
#     print("Expected: box, Actual: " + action_interpreter.llm_item_extraction(input1))
#     print("Expected: box, Actual: " + action_interpreter.llm_item_extraction(input2))
#     print("Expected: painting, Actual: " + action_interpreter.llm_item_extraction(input3))
#     print("Expected: painting, Actual: " + action_interpreter.llm_item_extraction(input4))
#     print("Expected: None, Actual: " + action_interpreter.llm_item_extraction(input5))
#     print("Expected: None, Actual: " + action_interpreter.llm_item_extraction(input6))

def test_validation():
    pass