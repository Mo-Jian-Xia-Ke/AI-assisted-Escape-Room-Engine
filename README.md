# Project name modified?
AI-assisted escape room engine

4.23 Todo List:
1. Objects dependent action list
2. Threshold hinting (e.g. 5 times failure -> give a hint? yes/no)
3. Try multi-label = true

# Environment: package_info.md
Remember to include MIT license
Comments: """ shoule be inside python class and functions!
UI-Manager

5.22 Todo List:
1. Finish //Hinting// and /Feedback/ for demo_2 [Partly_Done] [Partly_Done]
2. Create more puzzles and build demo_3
3. LLM & NLP evaluation (in action.py)

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
If confidence level > 0.75: accept
Else: LLM trigger

Report: different confidence level accuracy & time comparison

Puzzle examples: (Each can have one of the three modes above)
1. 数字谜题：[Done]
    “我的倒数是我自己的一半，正着看和反着看一样。” -> 121
    解方程或新定义运算等。
2. 密码谜题：[Done]
    Uifsf jt b tfdsfu npef -> （凯撒密码）There is a secret mode
3. 拼图谜题：(可以加code后套ind拼图)
    拼图成功后解谜，或是得到密码
4. 拨动时钟类谜题 [Done]
5. 书本排序类谜题

独立小游戏谜题：(ref Rusty Lake)
1. 音符敲击谜题
2. 点火顺序谜题
3. 拼图碎片复原 [Done]
4. 机关拼装（或旋转）