import enum
from abc import abstractmethod
import sys
import os

sys.path.append(os.path.abspath(".."))
from puzzle import Puzzle

class Dep_puzzle_type(enum.Enum):
    DIGITAL_LOCK = "digital_lock",
    CHAR_LOCK = "char_lock",
    CLOCK_PUZZLE = "clock_puzzle"

class DependentPuzzle(Puzzle):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def display(self):
        pass