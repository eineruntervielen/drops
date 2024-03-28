"""Source for further checkouts"""
from typing import Optional

from drops.core import DEvent, Event, EventCallback
from tests.examples.shop.checkout import make_checkout


def checkout_source_gen(num_checkout: int) -> EventCallback:
    counter = 0
    send = True

    def checkout_source(e: Optional[Event]) -> DEvent:
        nonlocal counter
        nonlocal send
        if counter >= num_checkout:
            send = False

        while send:
            counter += 1
            return DEvent(msg="register_checkout",
                          delay_s=0,
                          body={"checkout": make_checkout(counter)})
    return checkout_source

