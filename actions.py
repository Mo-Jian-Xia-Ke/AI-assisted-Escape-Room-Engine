# http://huggingface.co/facebook/bart-large-mnli

from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
sequence_to_classify = "What should I do now?"
candidate_labels = ['ask for clues', 'open the lock', 'open the drawer', 'look at the drawer']
result = classifier(sequence_to_classify, candidate_labels)
print(result)
# {'sequence': 'I want to use the key to open the door', 'labels': ['open the lock', 'ask for clues', 'move the table'], 'scores': [0.9374002814292908, 0.04698718339204788, 0.015612520277500153]}
# {'sequence': 'I want to check the drawer', 'labels': ['look at the drawer', 'open the drawer', 'ask for clues', 'open the lock'], 'scores': [0.6368684768676758, 0.33628571033477783, 0.018994150683283806, 0.007851657457649708]}
# {'sequence': 'What should I do now?', 'labels': ['ask for clues', 'open the lock', 'open the drawer', 'look at the drawer'], 'scores': [0.8905602693557739, 0.05941273644566536, 0.028227612376213074, 0.021799379959702492]}

import spacy
import en_core_web_sm

class Action:
    # def __init__(self, pull, push, drag, move, use_or_interact):
    #    pass
    def __init__(self):
        # self.candidate_labels = ['ask for clues', 'other', 'see the painting', 'unlock the door']
        self.candidate_labels = ['ask for clues', 'other']

    def word_net(self):
        pass

    def interpret(self, input):
        sequence_to_classify = input
        # candidate_labels = ['ask for clues', 'other', 'see the painting', 'see the door', 'see the key']
        results = classifier(sequence_to_classify, self.candidate_labels)
        print(results)
        result = results['labels'][0]
        return result
    
    def extract_noun(self, input):
        nlp = spacy.load("en_core_web_sm")
        nlp = en_core_web_sm.load()
        doc = nlp(input)
        nouns = []
        for w in doc:
            if w.pos_ == 'NOUN':
                nouns.append(w.text)
        return nouns
    
    def add_detected_label(self, nouns, items):
        # TODO: consider the case for deleting temporary labels
        for noun in nouns:
            for item in items:
                # TODO: modify the != here into a similarity test for accuracy
                if (item == None):
                    continue
                if (noun != item.get_name()):
                    print(item.get_name())
                    continue
                self.candidate_labels += item.label_list
    
    def add_label(self, new_label):
        # TODO: Check whether the similarity between the new_label and some existing labels are high
        self.candidate_labels.append(new_label)

    def del_label(self, old_label):
        # TODO: Only allow to delete customized labels
        self.candidate_labels.remove(old_label)

# Objects dependent action list
# Threshold hinting (e.g. 5 times failure -> give a hint? yes/no)

# Try multi-label = true
# need environment?