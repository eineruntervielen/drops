from types import MappingProxyType
from src.drops import Member, Event, EventQueue
from model.messages import Messages


class Bob(Member):
    default_config = MappingProxyType({
        'channels': {
            Messages.HELLO: '',
            Messages.GOOD_BY: ''
        }
    })
    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def hello(self, event: Event):
        print('hello from bob')
    
    def good_by(self, event: Event):
        print('goodby from bob')