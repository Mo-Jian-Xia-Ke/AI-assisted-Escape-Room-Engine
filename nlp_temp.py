# https://spacy.io/models

import spacy
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp("I want to use the key to open the door")
print([(w.text, w.pos_) for w in doc])

for w in doc:
    if w.pos_ == 'NOUN':
        print(w.text)