from model.alice import Alice
from model.bob import Bob
from enum import Enum


class Members(Enum):
    alice = Alice
    bob = Bob
