import pygame as pg

from agent import Agent, Action


class HumanAgent(Agent):
    def __init__(self, unit):
        super().__init__(unit)

    def choose_action(self, game_state):
        keys = pg.key.get_pressed()
        move_direction = [0, 0]

        if keys[pg.K_w]:
            move_direction[1] -= 1
        if keys[pg.K_s]:
            move_direction[1] += 1
        if keys[pg.K_a]:
            move_direction[0] -= 1
        if keys[pg.K_d]:
            move_direction[0] += 1

        ability_name = None
        if keys[pg.K_t] and not self.unit.casting_ability:
            ability_name = "magic_missile"
        elif keys[pg.K_1]:
            ability_name = "snare"
        elif keys[pg.K_2]:
            ability_name = "root"
        elif keys[pg.K_3]:
            ability_name = "stun"

        self.unit.logger.debug(
            f"HUMAN choose_actions({game_state}) -> move: {move_direction}, ability: {ability_name}"
        )

        return Action(move_direction, ability_name)
