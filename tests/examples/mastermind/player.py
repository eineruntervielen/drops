import random

from src.drops import Producer, Event


class Player(Producer):
    consumptions = ["choose_codeword", "win"]
    COLORS = "rgbyop"
    STRATEGY = "random"

    def __init__(self, name, event_queue):
        super().__init__(name, event_queue)
        self.publish(time=10, msg="start_game", possible_colors=self.COLORS, num_colors=4, tries=12)
        match self.STRATEGY:
            case "random":
                self.strategy = self._random_strategy

    def _random_strategy(self) -> str:
        return "".join(random.sample(population=self.COLORS, k=4))

    def win(self, event):
        print("fertig")

    def choose_codeword(self, event: Event):
        choice = self.strategy()
        self.publish(time=event.time + 1, msg="receive_code", codeword=choice)
