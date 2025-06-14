Goal:
    Escape the room!

Room:
    Items:
        1. A painting (Nailed to the wall -> unmovable)
            1.1 (invisible) Hidden Password
                ---investigate---> ? ---interact_with_2.3.1---> get password 0309
            1.2 A tilted corner ---investigate---> item 1.3 visible
            1.3 (invisible) a locked small chest (locked)
                ---investigate---> locked | ---interact_with_2.2.2.1---> item 1.4 visible
                                          | ---otherwise---> nothing happens
            1.4 (invisible) an open chest
                ---investigate---> item 1.4.1 appears
                    1.4.1 A door key (movable)
        2. A three-layer drawer (Too heavy -> unmovable)
            2.1 Layer 1: Empty
            2.2 Layer 2: 
                2.2.1 (visible) A password box (unmovable & can be further investigated)
                    ---investigate---> locked | ---input_correctly---> item 2.2.2 visible
                                              | ---input_wrongly---> nothing happens
                2.2.2 (invisible) An open box (unmovable & can be further investigated)
                    ---investigate---> item 2.2.2.1 appears
                        2.2.1.1 A small key (movable)
            2.3 Layer 3: 
                2.3.1 A magnifier (movable)
        3. A Door (locked)
            ---investigate---> locked | ---interact_with_1.4.1---> door open ---investigate---> YOU ESCAPE!
                                      | ---otherwise---> nothing happens

Solution:
    1. Open [2.3], Pick [2.3.1]
    2. Interact [1.1] with [2.3.1]
    3. Open [2.2], Interact [2.2.1] with Input {0309}
    4. Open [2.2.2], Pick [2.2.2.1]
    5. Investigate [1.2]
    6. Interact [1.3] with [2.2.2.1]
    7. Open [1.4], Pick [1.4.1]
    8. Interact [3] with [1.4.1]
    9. ESCAPE

------------------------------------------------------------------------

Goal:
    Escape the room!

Room:
    Items:
        1. A painting
            1.1 A tilted corner ---> 2
        2. Key
        3. A Door (locked)
            ---> use key to open