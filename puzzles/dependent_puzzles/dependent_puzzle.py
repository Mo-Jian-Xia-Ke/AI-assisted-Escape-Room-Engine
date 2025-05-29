import enum
from abc import abstractmethod

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