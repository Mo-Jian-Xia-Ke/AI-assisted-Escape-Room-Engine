class Engine:
    def __init__(self, state_of_the_game, correct_moves, objects, actions_maybe):
        pass

    def hint_generator(self):
        # state graphs?
        pass

    def action_interpreter(self):
        pass

    # LLM interface
    def feedback_generator(self):
        pass

    def room_description(self):
        pass

    # A big node represent the state graph: every item's current state and their potential next state
    # Problem: How to guarantee exist a way to escape? (final state)

    # let LLM to decide when to use forward / backward hinting

    # Simple action: NLP interpret; Complex/Error Prone action: LLM interpret

    # Rasa Models