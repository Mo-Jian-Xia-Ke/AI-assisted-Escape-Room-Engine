import enum
from abc import abstractmethod
from ..puzzle import Puzzle, PuzzleDependency

class IndepPuzzleType(enum.Enum):
    PURE_LOGIC = "pure_logic"
    JIGSAW = "jigsaw"

class IndependentPuzzle(Puzzle):
    puzzle_dependency = PuzzleDependency.INDEPENDENT_PUZZLE

    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def display(self):
        pass