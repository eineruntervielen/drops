import functools
from enum import Enum, unique
from typing import Callable, Hashable

import tomllib
from typing import Any

from drops.drops_old import Drops, Event
from importlib.machinery import SourceFileLoader


def load_cls_from_scenario(cls_path, cls_name):
    mod = SourceFileLoader(fullname=cls_path, path=cls_path).load_module()
    cls_ref = getattr(mod, cls_name)
    return cls_ref


def open_toml_scenario(scenario_name: str) -> dict[str, Any]:
    SCENARIO = scenario_name
    with open(SCENARIO, mode="rb") as t:
        return tomllib.load(t)


def load_scenario(scenario_name: str):
    data = open_toml_scenario(scenario_name)
    sim = Drops(**data.get('drops'))
    for handler in data.get("handlers"):
        cls_ref = load_cls_from_scenario(handler['file'], handler['class'])
        sim.register_class(cls_ref)

    for cb in data.get("callbacks"):
        cb_ref = load_cls_from_scenario(cb['file'], cb['name'])
        sim.register_callback(cb_ref, cb['msgs'])
    return sim


def create_logger(log_func: Callable[[Hashable, str, Event], None]):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            msg = func.__name__
            class_name, event = args
            cls = str(class_name)[:-2]  # remove parenthesis
            log_func(msg, cls, event)
            return func(*args, **kwargs)

        return wrapper

    return inner


@unique
class DropsMessage(Enum):
    """An implementation of a dx-centered Enum.
    Since DropsMessage's pseudo-callbacks are by design the lowercase
    of the DropsMessage name, the value of the enum is of no interest.
    Therefore, one can use it like this:

    class Messages(DropsMessage):
        HELLO = ()
        GOOD_BY = ()
        HOW_ARE_YOU = ()
    """

    def __new__(cls):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__) + 1
        return obj

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}.{self.name}>'

    def __str__(self) -> str:
        return f"{self.name}"
# class DropsHTTPRequestHandler(SimpleHTTPRequestHandler):
#     """
#     recepie:
#
#     https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
#     """
#     record_provider: any
#
#     def do_GET(self):
#         if self.path == '/':
#             try:
#                 self.send_response(200)
#                 self.send_header("Content-type", "text/html")
#                 html = f"<html><head></head><body><h1>Hello {DropsHTTPRequestHandler.record_provider}!</h1></body></html>"
#             except:
#                 self.send_response(404)
#         self.end_headers()
#         self.wfile.write(bytes(html, "utf8"))
#         # self.wfile.write(bytes(f'{DropsHTTPRequestHandler.record_provider}', 'utf-8'))
#

#
#
# # class Producer:
# #     counter = count()
# #     consumptions: dict[DropsMessage, MessageFilter] = {}
# #
# #     def __init__(self, name: str, event_queue: EventQueue):
# #         self.component_id: int = next(self.counter)
# #         self.name: str = name
# #         self.event_queue: EventQueue = event_queue
# #
# #         self._check_consumptions()
# #         self._subscribe()
# #         self._check_reactions()
# #
# #     def _check_consumptions(self):
# #         if not self.consumptions:
# #             print(NotImplementedError(
# #                 f'The component {self.name} has no subscriptions. Are you shure that was intended?'
# #             ))
# #
# #     def _subscribe(self):
# #         for subscription in self.consumptions:
# #             self.event_queue.channels[subscription].append(self)
# #
# #     def _check_reactions(self):
# #         for subscription in self.consumptions:
# #             reaction_name: str = str(subscription).lower()
# #             if not hasattr(self, reaction_name):
# #                 raise NotImplementedError(
# #                     f'Member {self} needs to implement a reaction for the subscription {subscription}'
# #                 )
# #
# #     def publish(self, *, time: DropsTime, msg: DropsMessage | str, **kwargs):
# #         """Inserts an upcoming Event into the EventQueue.
# #
# #         Args:
# #             time (DropsTime): Future point in time when the event happens
# #             msg: (DropsMessage): Message that carries the information
# #             **kwargs: The rest of the attributes to create an event
# #         """
# #         sargs = locals()
# #         self.event_queue.put(
# #             Event(time=time, msg=msg, sender=self, **sargs['kwargs'])
# #         )
# class ScenarioLoader:
#
#     def serve(self, host: str, port: int):
#         DropsHTTPRequestHandler.record_provider = self
#         httpd = HTTPServer((host, port), DropsHTTPRequestHandler)
#         thread = threading.Thread(target=self.run)
#         try:
#             thread.start()
#             httpd.serve_forever()
#         except KeyboardInterrupt as kbd:
#             print(kbd)
#
#     def _load_modules(self):
#         # todo this needs to be understood in greater detail but looks awesome
#         spec_members = importlib.util.spec_from_file_location(
#             "members", self.scenario_path / 'model/members.py')
#         spec_messages = importlib.util.spec_from_file_location(
#             "messages", self.scenario_path / 'model/messages.py')
#         members = importlib.util.module_from_spec(spec_members)
#         messages = importlib.util.module_from_spec(spec_messages)
#         sys.modules["members"] = members
#         sys.modules["messages"] = messages
#         spec_members.loader.exec_module(members)
#         spec_messages.loader.exec_module(messages)
#         self.members = members.Members
#         self.messages = messages.Messages
#
#     def _register_members(self):
#         for member in self.members:
#             member_class = member.get("member")
#             member_name = member.get("name")
#             for msg in member_class.subscriptions:
#                 self.event_queue.open_new_channel(msg)
#             member_class(name=member_name, event_queue=self.event_queue)
