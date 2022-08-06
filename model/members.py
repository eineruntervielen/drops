from model.alice import Alice
from model.bob import Bob
from enum import Enum


class Members(Enum):
    ALICE = Alice
    BOB = Bob
