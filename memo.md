# Project name:
AI-assisted escape room engine

4.23 Todo List:
1. Objects dependent action list
2. Threshold hinting (e.g. 5 times failure -> give a hint? yes/no)
3. Try multi-label = true

# Environment: requirements.txt
Remember to include MIT license
Comments: """ shoule be inside python class and functions!
UI-Manager

5.22 Todo List:
1. Finish //Hinting// and /Feedback/ for demo_2 [Partly_Done] [Partly_Done]
2. Create more puzzles and build demo_3
3. LLM & NLP evaluation

4. Negative prompting in item_filler.py [Partly_Done]
5. UI-Design
6. Strict digital lock: Only "see code first then type code" -> success
   Lazy digital lock: As soon as "type code" -> success
   Adaptive digital lock (default): Generate code that avoid initial guesses, or guess all -> success ("Wow so hard you've tried!") [Waitlist]

5.29 Todo List:
Implement Hinting Manager [Problem: Sometimes trigger the action label, but not 'ask for hint', need the hybrid approach implement!]
From json to yml file?

6.5:
Correct Label + 2-3 Interrupt label
If confidence level > 0.5: accept
Else: LLM trigger

Report: different confidence level accuracy & time comparison
