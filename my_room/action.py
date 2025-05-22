# http://huggingface.co/facebook/bart-large-mnli

import transformers

import spacy
import en_core_web_sm

import item_filler
# classifier usage example:
# sequence_to_classify = "What should I do now?"
# candidate_labels = ['ask for clues', 'open the lock', 'open the drawer', 'look at the drawer']
# result = classifier(sequence_to_classify, candidate_labels)

# result examples:
# {'sequence': 'I want to use the key to open the door', 'labels': ['open the lock', 'ask for clues', 'move the table'], 'scores': [0.9374002814292908, 0.04698718339204788, 0.015612520277500153]}
# {'sequence': 'I want to check the drawer', 'labels': ['look at the drawer', 'open the drawer', 'ask for clues', 'open the lock'], 'scores': [0.6368684768676758, 0.33628571033477783, 0.018994150683283806, 0.007851657457649708]}
# {'sequence': 'What should I do now?', 'labels': ['ask for clues', 'open the lock', 'open the drawer', 'look at the drawer'], 'scores': [0.8905602693557739, 0.05941273644566536, 0.028227612376213074, 0.021799379959702492]}

class Action:
    def __init__(self):
        self.candidate_labels = ['ask for hint', 'other']
        self.classifier = transformers.pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def word_net(self):
        pass

    # Return the label with the highest correspondent value, i.e. the top label
    def interpret(self, input, labels):
        results = self.classifier(input, labels)
        print(results)
        result = results['labels'][0]
        return result
    
    # Given an input sentence, return all the nouns as a list
    def extract_noun(self, input):
        nlp = spacy.load("en_core_web_sm")
        nlp = en_core_web_sm.load()
        doc = nlp(input)
        nouns = []
        for w in doc:
            if w.pos_ == 'NOUN':
                nouns.append(w.text)
        return nouns
    
    # Add labels of item whose name corresponds to the noun in the nouns, then return the updated label list
    def update_labels(self, nouns, items):
        # A shallow copy of the list by slicing
        added_labels = self.candidate_labels[:]
        for noun in nouns:
            for key in items:
                item = items[key]
                # If item is invisible now, skip this item.
                if item.check_invisible():
                    continue

                # TODO: modify the == here into a similarity test for accuracy (word net?)
                if noun == key:
                    # TODO: How to deal with end state label for feedback?
                    if item.check_end_state():
                        added_labels.append(item.get_name())
                        break

                    if not item.get_current_label():
                        item.set_current_label(item_filler.label_generator(item))
                    added_labels.append(item.get_current_label())
                    print(noun)
                    break
        return added_labels

# Objects dependent action list
# Threshold hinting (e.g. 5 times failure -> give a hint? yes/no)

# Try multi-label = true


# ----------------------------------------------------------------- #

# Unit tests
def test_extract_noun(item):
    return label_generator(item)