import datetime as dt

from types import MappingProxyType
from src.drops import Member, Event, EventQueue
from examples.aliceandbob.model.messages import Messages


class Vender(Member):
    default_config = MappingProxyType({
        'coin_detection_probability': 0.5,
        'channels': {
            Messages.COIN_INSERTED: ''
        }
    })

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.coin_detection_probability = self.default_config['coin_detection_probability']
    
    def coin_inserted(self, e: Event):
        print('coin inserted says vender')