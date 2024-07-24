import pygame as pg

from agent import Agent


class HumanAgent(Agent):
    def __init__(self, unit):
        super().__init__(unit)

    def choose_action(self, game_state):
        keys = pg.key.get_pressed()
        actions = []

        if keys[pg.K_w]:
            actions.append("move_up")
        if keys[pg.K_s]:
            actions.append("move_down")
        if keys[pg.K_a]:
            actions.append("move_left")
        if keys[pg.K_d]:
            actions.append("move_right")
        if keys[pg.K_t] and not self.unit.casting_ability:
            actions.append("cast_magic_missile")
        if keys[pg.K_1]:
            actions.append("use_snare")
        if keys[pg.K_2]:
            actions.append("use_root")
        if keys[pg.K_3]:
            actions.append("use_stun")

        return actions
