import sys

import pygame as pg

from unit import Unit


class Battle:
    is_active: bool
    render: bool
    temp_counter: int
    paused: bool
    fetch_input: bool
    units: list[Unit] = []

    def __init__(self, render: bool = True):
        self.is_active = True
        self.render = render
        self.temp_counter = 0
        self.paused = True
        self.fetch_input = True

        self.units.append(Unit(player=True, initial_pos=[100, 100]))
        self.units.append(Unit(player=False, initial_pos=[400, 300]))

    def tick(self) -> None:
        if self.fetch_input:
            # process events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.paused = not self.paused
                        print(f"{self.paused=}")

        # get inputs, move entities, check collisions, update game data
        if not self.paused:
            self.temp_counter += 1

        if self.temp_counter > 1_000:
            self.is_active = False
