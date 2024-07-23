# imports from standard libary
from typing import Optional

# imports from this project
from battle import Battle
from canvas import Canvas


class Game:
    current_battle: Optional[Battle]
    canvas: Canvas

    def __init__(self):
        self.current_battle = None
        self.canvas = Canvas()
        pass

    def run(self):
        if self.current_battle is None:
            self.current_battle = Battle()

        print("starting new battle")

        while self.current_battle.is_active:
            self.current_battle.tick()

            if self.current_battle.render:
                self.canvas.draw(self.current_battle.units)

        print("battle done")
