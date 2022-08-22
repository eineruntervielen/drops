from enum import Enum

from examples.movie_renege.model.moviegoer import Moviegoer
from examples.movie_renege.model.theater import Theater


class Members(Enum):
    MOVIEGOER = Moviegoer
    THEATER = Theater
