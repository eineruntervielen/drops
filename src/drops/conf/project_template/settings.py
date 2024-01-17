import functools
import logging
from asyncio import Event
from typing import Callable, Hashable

from rich.logging import RichHandler

# Standard directory where the scenarios are listed
DIR_SCENARIO = "scenarios"
# Standard directory where the domain model is defined
DIR_DOMAIN = "domain"
# Standard scenario file-type
TYPE_SCENARIO = "toml"
# Top level logging for printing
FORMAT = "%(asctime)s  %(message)s"
HANDLER = RichHandler(show_level=False, show_time=False)
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[HANDLER]
)
logger = logging.getLogger("rich").info


