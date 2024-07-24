import sys
import pygame as pg
import math

from unit import Unit
from ability import Projectile


class Battle:
    def __init__(self, render: bool = True):
        self.is_active = True
        self.render = render
        self.paused = True
        self.fetch_input = True

        self.units = [
            Unit(player=True, initial_pos=[100, 100]),
            Unit(player=False, initial_pos=[400, 300]),
        ]

    def tick(self, dt: float) -> None:
        enemy = self.units[1]
        player = self.units[0]

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

                    if not self.paused:
                        if event.key == pg.K_t:
                            if not player.casting_ability:
                                player.start_casting("magic_missile", enemy)
                        elif event.key == pg.K_1:
                            player.use_ability("snare", enemy)
                        elif event.key == pg.K_2:
                            player.use_ability("root", enemy)
                        elif event.key == pg.K_3:
                            player.use_ability("stun", enemy)

        # get inputs, move entities, check collisions, update game data
        if not self.paused:
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
                    player.move(direction, dt)

            # Update casting and CC effects
            for unit in self.units:
                if unit.update_cast(dt):
                    print("cast completed")
                unit.update_cc(dt)

            # AI movement and melee attack
            dist_to_player = math.sqrt(
                (enemy.pos[0] - player.pos[0]) ** 2
                + (enemy.pos[1] - player.pos[1]) ** 2
            )

            if dist_to_player > enemy.abilities["melee_attack"].range:
                enemy.move_towards(player.pos, dt)
            else:
                enemy.use_ability("melee_attack", player)

            # Move and draw projectiles
            for unit in self.units:
                for projectile in unit.projectiles:
                    projectile.move(dt)
                    if self.check_collision(projectile, enemy):
                        if unit.completed_ability:
                            enemy.current_hp -= unit.completed_ability.damage
                        unit.projectiles.remove(projectile)

            if enemy.current_hp <= 0:
                print("Enemy died")
                self.is_active = False

            if player.current_hp <= 0:
                print("Player died")
                self.is_active = False

    def check_collision(self, projectile, target: Unit) -> bool:
        dist = math.sqrt(
            (projectile.pos[0] - target.pos[0]) ** 2
            + (projectile.pos[1] - target.pos[1]) ** 2
        )
        return dist < target.radius
