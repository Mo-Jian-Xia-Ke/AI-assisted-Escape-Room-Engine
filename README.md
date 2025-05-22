Object Types:

[Look]
1. Key Type
    [Use]
2. Lock Type
    [# To be interacted] [# attachable]
    [Unlock]
3. Container Type
    [Open] [Close] # Can attach lock
    [Pull?] [Push?]
4. Investigatable Type
    [Investigate...]

Todo List:
1. Objects dependent action list
2. Threshold hinting (e.g. 5 times failure -> give a hint? yes/no)
3. Try multi-label = true

# need environment?

State Template:

State (Object):
    State Index:
        1
    State Description:
        A closet with an open drawer
    Pre-action Description:
        Open the drawer
    Labels:
        ...
    Post-actions:
        A -> State 2
        B -> State 3
        ...