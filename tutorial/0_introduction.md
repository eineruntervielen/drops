# Drops

is a progressive python framework for building large-scale,
object-oriented discrete-event simulation models with a focus on high cohesion
and a great developer-experience.

## Minimum example

```python
from drops import DropsMessage, DropsComponent, MessageFilter, Event, EventQueue


class Messages(DropsMessage):
    HELLO = ()
    GOOD_BY = ()


class Alice(DropsComponent):
    subscriptions = {
        Messages.GOOD_BY: MessageFilter(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.share(time=0, msg=Messages.HELLO)

    def good_by(self, e: Event):
        print(f'Good by {e.sender}')


class Bob(DropsComponent):
    subscriptions = {
        Messages.HELLO: MessageFilter(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def hello(self, e: Event):
        print(f'Hello {e.sender}')
        self.share(time=e.time + 1, msg=Messages.GOOD_BY)


```