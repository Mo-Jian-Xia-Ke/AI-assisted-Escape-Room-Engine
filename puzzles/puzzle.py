from abc import ABC, abstractmethod
import enum

class PuzzleDependency(enum.Enum):
    DEPENDENT_PUZZLE = "dependent_puzzle"
    INDEPENDENT_PUZZLE = "independent_puzzle"

# Abstract class Puzzle for the subclass to inherit
class Puzzle(ABC):
    # Subclass must be set its puzzle type
    @abstractmethod
    def __init__(self):
        pass

    # Subclass must be able to display the puzzle
    # Return True indicates puzzle solved, the item containing puzzle can be proceeded to the next state
    # Return False indicates puzzle remains unsolved, but to leave the puzzle temporarily
    @abstractmethod
    def display(self):
        pass
