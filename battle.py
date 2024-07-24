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

    def tick(self, dt: float) -> None:
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
                    elif event.key == pg.K_t:
                        if self.units[0].casting:
                            self.units[0].cancel_cast()

                        self.units[0].start_casting(1)  # start casting a 1s spell

        # get inputs, move entities, check collisions, update game data
        if not self.paused:
            self.temp_counter += 1

            if self.fetch_input:
                # get WASD input for moving player
                keys = pg.key.get_pressed()
                direction = [0, 0]
                if keys[pg.K_w]:
                    direction[1] -= 1
                if keys[pg.K_s]:
                    direction[1] += 1
                if keys[pg.K_a]:
                    direction[0] -= 1
                if keys[pg.K_d]:
                    direction[0] += 1

                if abs(direction[0]) + abs(direction[1]) > 0:
                    self.units[0].move(direction, dt)

            # Update casting
            for unit in self.units:
                if unit.casting:
                    if unit.update_cast(dt):
                        print("cast completed")

        if self.temp_counter > 100_000:
            self.is_active = False
