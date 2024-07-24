import math
import time
from ability import Ability, Projectile
from typing import Optional


class Unit:
    projectiles: list[Projectile]

    def __init__(self, player: bool, initial_pos: list[float], max_hp: int = 100):
        self.pos = initial_pos
        self.player = player
        self.radius = 20
        self.speed = 100  # Adjust for reasonable movement
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.casting_ability: Optional[Ability] = None
        self.completed_ability: Optional[Ability] = None
        self.abilities = {
            "magic_missile": Ability(
                "Magic Missile",
                cast_time=1,
                cooldown=0,
                damage=20,
                is_instant=False,
                off_gcd=False,
                color=(128, 0, 128),
            ),
            "melee_attack": Ability(
                "Melee Attack",
                cast_time=0,
                cooldown=2,  # 2 second swing timer
                damage=10,
                is_instant=True,  # shouldnt this be mutex with cooldown>0?
                off_gcd=True,
                color=(255, 0, 0),
                range=50,  # Melee range
            ),
            # Add more abilities as needed
        }
        self.projectiles = []

    def move(self, direction: list[float], dt: float) -> None:
        norm = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if norm != 0:
            direction[0] /= norm
            direction[1] /= norm

        dx = direction[0] * self.speed * dt
        dy = direction[1] * self.speed * dt

        self.pos[0] += dx
        self.pos[1] += dy

        if self.casting_ability:
            self.cancel_cast()

    def move_towards(self, target_pos: list[float], dt: float):
        direction = [target_pos[0] - self.pos[0], target_pos[1] - self.pos[1]]
        self.move(direction, dt)

    def start_casting(self, ability_name: str):
        ability = self.abilities.get(ability_name)
        if ability and ability.can_use(time.time()):
            self.casting_ability = ability
            self.casting_ability.cast_time_elapsed = 0

    def update_cast(self, dt: float):
        if self.casting_ability:
            self.casting_ability.cast_time_elapsed += dt
            if self.casting_ability.cast_time_elapsed >= self.casting_ability.cast_time:
                self.casting_ability.last_used = time.time()
                self.projectiles.append(
                    Projectile(self.pos, [400, 300], self.casting_ability.color)
                )  # Example target
                self.completed_ability = self.casting_ability
                self.casting_ability = None
                return True  # indicate cast completion
        return False  # cast not completed

    def cancel_cast(self):
        self.casting_ability = None

    def use_ability(self, ability_name: str, target: Optional["Unit"] = None):
        ability = self.abilities.get(ability_name)
        if ability and ability.is_instant and ability.can_use(time.time()):
            if ability.range > 0 and target:
                distance = math.sqrt(
                    (self.pos[0] - target.pos[0]) ** 2
                    + (self.pos[1] - target.pos[1]) ** 2
                )
                if distance > ability.range:
                    return 0  # target out of range (WTF is return value)
            if target:
                target.current_hp -= ability.damage
            ability.last_used = time.time()
            return ability.damage
        return 0
