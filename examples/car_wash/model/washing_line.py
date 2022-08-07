import datetime as dt

from types import MappingProxyType
from src.drops import Member, Event, EventQueue
from model.logger import log
from model.messages import Messages


class WashingLine(Member):
    default_config = MappingProxyType({
        'channels': {}
    })

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
