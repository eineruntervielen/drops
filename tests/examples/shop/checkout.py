import random
from typing import NamedTuple


class Checkout(NamedTuple):
    """Each checkout has an individual number, and the cashier has an average speed."""
    checkout_id: int
    speed: float


def make_checkout(counter: int) -> Checkout:
    """Create a checkout

    Args:
        counter: ID that the Checkout being created should have.

    Returns: A new checkout with random speed

    """
    return Checkout(checkout_id=counter, speed=round(random.uniform(0.2, 1), 2))
