from types import MappingProxyType
from src.drops import Member, Event
from model.messages import Messages


class Alice(Member):
    default_config = MappingProxyType({
        'channels': {
            Messages.HELLO: '',
            Messages.GOOD_BY: ''
        }
    })
    def __init__(self, name: str):
        super().__init__(name)
    
    def hello(event: Event):
        print('hello from alic')
    
    def good_by(event: Event):
        print('goodby from alice')