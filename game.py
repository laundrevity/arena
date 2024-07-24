from typing import Optional
import time

from battle import Battle
from canvas import Canvas


class Game:
    current_battle: Optional[Battle]
    canvas: Canvas
    debug: bool

    def __init__(self, debug: bool = False):
        self.current_battle = None
        self.canvas = Canvas()
        self.debug = debug

    def run(self):
        if self.current_battle is None:
            self.current_battle = Battle()

        if self.debug:
            print("starting new battle")

        last_time = time.time()

        while self.current_battle.is_active:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            self.current_battle.tick(dt)

            if self.current_battle.render:
                self.canvas.draw(self.current_battle.units, self.current_battle.paused)
        if self.debug:
            print("battle done")

    def draw_debug_info(self):
        # Implement debug info display
        pass
