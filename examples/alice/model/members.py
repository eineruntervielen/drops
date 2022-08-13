from examples.alice.model.alice import Alice
from examples.alice.model.vendor import Vendor
from enum import Enum


class Members(Enum):
    ALICE = Alice
    VENDOR = Vendor
