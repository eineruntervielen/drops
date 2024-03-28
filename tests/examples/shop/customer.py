import random
from typing import NamedTuple


class Customer(NamedTuple):
    """A customer of the shop. A customer has a unique customer_id and a certain
    number of products.
    """
    customer_id: int
    number_products: int


def make_customer(counter: int) -> Customer:
    """Create a customer

    Args:
        counter: Unique customer id that the customer being created should have.

    Returns: A new customer

    """
    return Customer(customer_id=counter, number_products=random.randint(1, 50))
