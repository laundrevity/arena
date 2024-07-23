import pygame as pg


class Battle:
    is_active: bool
    render: bool
    temp_counter: int
    paused: bool
    fetch_input: bool

    def __init__(self, render: bool = True):
        self.is_active = True
        self.render = render
        self.temp_counter = 0
        self.paused = True
        self.fetch_input = True

    def tick(self) -> None:
        # get inputs, move entities, check collisions, update game data
        if not self.paused:
            self.temp_counter += 1

        if self.temp_counter > 1_000:
            self.is_active = False

        # NOTE: this is only relevant in case the battle includes a human!
        # redundant to have BOTH attributes render and fetch_input, no?
        # not necessarily, in case we wanted to watch bot games
        if self.fetch_input:
            # print("fetching input")
            keys = pg.key.get_pressed()

            # limit to 60 FPS
            pg.time.Clock().tick(60)

            if keys[pg.K_w]:
                self.paused = not self.paused
                print("SPACE")
