import enum
from abc import abstractmethod
import sys
import os

sys.path.append(os.path.abspath(".."))
from puzzle import Puzzle

class Indep_puzzle_type(enum.Enum):
    PURE_LOGIC = "pure_logic",
    JIGSAW = "jigsaw"

class IndependentPuzzle(Puzzle):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def display(self):
        pass