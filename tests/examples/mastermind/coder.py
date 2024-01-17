import random
from dataclasses import dataclass

from drops import Producer

C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_WHITE = "\033[97m"
ENDC = "\033[0m"


@dataclass
class ReceiveCodeEvent:
    time: int
    codeword: str


@dataclass
class StartGameEvent:
    time: int
    possible_colors: str
    max_tries: int
    num_colors: int = 4
    tries: int = 12


class Coder(Producer):
    consumptions = [
        "receive_code",
        "start_game"
    ]

    def __init__(self, name, event_queue):
        super().__init__(name, event_queue)
        self.tries = 0
        self.possible_colors = ""
        self.input_history = []
        self.color_code = ""

    def start_game(self, event: StartGameEvent):
        print("Mastermind:  Lets go!")
        self.possible_colors = event.possible_colors
        self.tries = event.tries
        self.color_code = "".join(random.sample(population=self.possible_colors, k=event.num_colors))
        self.publish(time=event.time + 1, msg=f"choose_codeword")

    def check_if_game_won(self, user_choice: str) -> bool:
        """When the user has chosen the correct set of colors the game ends,
        otherwise the hints are printed to stdout

        :param user_choice: Combination of colors from stdin
        :return: True iff won
        """
        if won := user_choice == self.color_code:
            print(C_GREEN + "Game over:\n You win!" + ENDC)
            return won

        count_white = 0
        count_red = 0
        for position, color in enumerate(user_choice):
            if color == self.color_code[position]:
                count_red += 1
            elif color in self.color_code:
                count_white += 1

        print(C_RED + "█ " * count_red + ENDC + C_WHITE + "█ " * count_white + ENDC)
        return False

    def receive_code(self, event: ReceiveCodeEvent):
        t = event.time
        user_choice = event.codeword
        self.tries += 1
        self.input_history.append(user_choice)
        if self.check_if_game_won(user_choice):
            self.publish(time=t + 1, msg="win")
        else:
            self.publish(time=t + 1, msg="choose_codeword")
