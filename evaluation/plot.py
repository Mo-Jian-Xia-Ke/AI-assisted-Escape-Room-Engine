# import matplotlib.pyplot as plt
# import numpy as np

# x_labels = ['Clear', 'Moderate', 'Vague']
# x = np.arange(len(x_labels)) 

# line1 = [0.84, 0.36, 0.16] 
# line2 = [0.77, 0.58, 0.52] 
# line3 = [0.51, 0.60, 0.80] 
# line4 = [0.81, 0.66, 0.56] 

# plt.figure(figsize=(8, 6))

# plt.plot(x, line1, marker='o', label='Classic NLP Mode', linestyle='-', color='blue')
# plt.plot(x, line2, marker='o', label='Transformer-Based NLP Mode', linestyle='-', color='green')
# plt.plot(x, line3, marker='o', label='LLM Mode', linestyle='-', color='red')
# plt.plot(x, line4, marker='o', label='Hybrid Mode', linestyle='-', color='purple')

# plt.title('Accuracy Across Clarity Levels', fontsize=14)
# plt.xlabel('Instruction Clarity', fontsize=12)
# plt.ylabel('Accuracy', fontsize=12)

# plt.xticks(x, x_labels)
# plt.legend()
# plt.grid(True, linestyle='--', alpha=0.6)

# plt.tight_layout()

# # save_path = 'accuracy_comparison.png' 
# # plt.savefig(save_path, dpi=300, bbox_inches='tight') 

# plt.show()

import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp(u'Use the key to open the door.')
displacy.serve(doc, style="dep")