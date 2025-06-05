import enum
from abc import abstractmethod
import sys
import os

# sys.path.append(os.path.abspath(".."))
from ..puzzle import Puzzle, PuzzleDependency

class DepPuzzleType(enum.Enum):
    DIGITAL_LOCK = "digital_lock"
    CHAR_LOCK = "char_lock"
    CLOCK_PUZZLE = "clock_puzzle"

class DependentPuzzle(Puzzle):
    puzzle_dependency = PuzzleDependency.DEPENDENT_PUZZLE

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def display(self):
        pass
    
    # Dependent puzzles rely on a specific code
    # Other items need get_code to get the code to show in their states (like a painting)
    @abstractmethod
    def get_code(self):
        pass