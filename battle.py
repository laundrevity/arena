import sys
import pygame as pg
import math
from logging import Logger

from unit import Unit
from ability import Projectile


class Battle:
    def __init__(
        self,
        logger: Logger,
        player_role=None,
        ai_role=None,
        ai2_role=None,
        ai_vs_ai=False,
        render: bool = True,
    ):
        self.is_active = True
        self.render = render
        self.paused = True
        self.fetch_input = not ai_vs_ai
        self.logger = logger

        if ai_vs_ai:
            self.units = [
                Unit(logger, player=False, initial_pos=[100, 100], role=ai_role),
                Unit(logger, player=False, initial_pos=[400, 300], role=ai2_role),
            ]
        else:
            self.units = [
                Unit(logger, player=True, initial_pos=[100, 100], role=player_role),
                Unit(logger, player=False, initial_pos=[400, 300], role=ai_role),
            ]

        self.logger.info(f"Battle setup: {self.units}")

    def tick(self, dt: float) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused
                    self.logger.debug(f"Game {'paused' if self.paused else 'resumed'}")

                if not self.paused and self.fetch_input:
                    player = self.units[0]
                    if event.key == pg.K_t:
                        if not player.casting_ability:
                            self.logger.info("Player starts casting Magic Missle")
                            player.start_casting("magic_missile", self.units[1])
                    elif event.key == pg.K_1:
                        self.logger.info("Player uses Snare")
                        player.use_ability("snare", self.units[1])
                    elif event.key == pg.K_2:
                        self.logger.info("Player uses Root")
                        player.use_ability("root", self.units[1])
                    elif event.key == pg.K_3:
                        self.logger.info("Player uses Stun")
                        player.use_ability("stun", self.units[1])

        if not self.paused:
            if self.fetch_input:
                player = self.units[0]
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
                    player.move(direction, dt)

            # Update casting and CC effects
            for unit in self.units:
                if unit.update_cast(dt):
                    self.logger.info(
                        f"{unit} completed casting {unit.completed_ability.name}"
                    )
                unit.update_cc(dt)

                for unit in self.units:
                    for projectile in unit.projectiles:
                        projectile.move(dt)
                        for target in self.units:
                            if target != unit and self.check_collision(
                                projectile, target
                            ):
                                target.current_hp -= unit.completed_ability.damage
                                unit.projectiles.remove(projectile)
                                self.logger.info(
                                    f"{unit} hits {target} with {unit.completed_ability.name}"
                                )

            if self.units[1].current_hp <= 0:
                self.logger.info("Enemy died")
                self.is_active = False

            if self.units[0].current_hp <= 0:
                self.logger.info("Player died")
                self.is_active = False

            if len(self.units) == 2:
                if not self.fetch_input:
                    self.update_ai(self.units[0], self.units[1], dt)
                    self.update_ai(self.units[1], self.units[0], dt)
                else:
                    self.update_ai(self.units[1], self.units[0], dt)

    def update_ai(self, ai_unit: Unit, target: Unit, dt: float):
        if ai_unit.role == "melee":
            dist_to_target = math.sqrt(
                (ai_unit.pos[0] - target.pos[0]) ** 2
                + (ai_unit.pos[1] - target.pos[1]) ** 2
            )

            if dist_to_target > ai_unit.abilities["melee_attack"].range:
                ai_unit.move_towards(target.pos, dt)
            else:
                ai_unit.use_ability("melee_attack", target)

        elif ai_unit.role == "caster":
            if ai_unit.casting_ability is None:
                for spell_name in ["magic_missile", "stun", "root", "snare"]:
                    if ai_unit.can_use(spell_name):
                        ai_unit.start_casting(spell_name, target)

    def check_collision(self, projectile, target: Unit) -> bool:
        dist = math.sqrt(
            (projectile.pos[0] - target.pos[0]) ** 2
            + (projectile.pos[1] - target.pos[1]) ** 2
        )
        return dist < target.radius
