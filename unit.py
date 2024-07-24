import math
import time
from ability import Ability, Projectile
from typing import Optional


class Unit:
    projectiles: list[Projectile]
    target: Optional["Unit"]  # Use a forward reference as a string

    def __init__(
        self, player: bool, initial_pos: list[float], role: str, max_hp: int = 100
    ):
        self.pos = initial_pos
        self.player = player
        self.radius = 20
        self.base_speed = 100  # Base speed before CC effects
        self.speed = self.base_speed  # Adjust for reasonable movement
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.role = role
        self.casting_ability: Optional[Ability] = None
        self.completed_ability: Optional[Ability] = None
        self.target = None
        self.projectiles = []
        self.cc_effects = {"snare": 0, "root": 0, "stun": 0}
        self.abilities = self.get_abilities_for_role(role)

    def get_abilities_for_role(self, role: str):
        abilities = {
            "caster": {
                "magic_missile": Ability(
                    "Magic Missile",
                    cast_time=1,
                    cooldown=0,
                    damage=20,
                    is_instant=False,
                    off_gcd=False,
                    color=(128, 0, 128),
                ),
                "snare": Ability(
                    "Snare",
                    cast_time=0,
                    cooldown=10,
                    damage=0,
                    is_instant=True,
                    off_gcd=True,
                    color=(0, 0, 255),
                    range=150,
                    cc_type="snare",
                ),
                "root": Ability(
                    "Root",
                    cast_time=0,
                    cooldown=15,
                    damage=0,
                    is_instant=True,
                    off_gcd=True,
                    color=(0, 255, 0),
                    range=150,
                    cc_type="root",
                ),
                "stun": Ability(
                    "Stun",
                    cast_time=0,
                    cooldown=20,
                    damage=0,
                    is_instant=True,
                    off_gcd=True,
                    color=(255, 0, 0),
                    range=150,
                    cc_type="stun",
                ),
            },
            "melee": {
                "melee_attack": Ability(
                    "Melee Attack",
                    cast_time=0,
                    cooldown=2,
                    damage=10,
                    is_instant=True,
                    off_gcd=True,
                    color=(255, 0, 0),
                    range=50,
                )
            },
        }
        return abilities.get(role, {})

    def move(self, direction: list[float], dt: float) -> None:
        if self.cc_effects["root"] > 0 or self.cc_effects["stun"] > 0:
            return  # Cannot move if rooted or stunned

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

    def start_casting(self, ability_name: str, target: Optional["Unit"] = None):
        if self.cc_effects["stun"] > 0:
            return  # Cannot cast if stunned

        ability = self.abilities.get(ability_name)
        if ability and ability.can_use(time.time()):
            self.casting_ability = ability
            self.casting_ability.cast_time_elapsed = 0
            # set target to remember for when cast completes
            self.target = target

    def update_cast(self, dt: float):
        if self.casting_ability:
            self.casting_ability.cast_time_elapsed += dt
            if self.casting_ability.cast_time_elapsed >= self.casting_ability.cast_time:
                if self.target is None:
                    print("Cannot complete cast - no valid target!")
                    return False

                self.casting_ability.last_used = time.time()
                self.projectiles.append(
                    Projectile(self.pos, self.target.pos, self.casting_ability.color)
                )
                self.completed_ability = self.casting_ability
                self.casting_ability = None
                return True  # indicate cast completion
        return False  # cast not completed

    def cancel_cast(self):
        self.casting_ability = None

    def use_ability(self, ability_name: str, target: Optional["Unit"] = None):
        print(f"use_ability({ability_name})")
        ability = self.abilities.get(ability_name)
        if ability and ability.is_instant and ability.can_use(time.time()):
            if ability.range > 0 and target:
                distance = math.sqrt(
                    (self.pos[0] - target.pos[0]) ** 2
                    + (self.pos[1] - target.pos[1]) ** 2
                )
                if distance > ability.range:
                    print(f"target out of range: {distance=} > {ability.range=}")
                    return 0  # target out of range (WTF is return value)

            if ability.cc_type and target:
                target.apply_cc(ability.cc_type, 5)  # apply CC effect for 5 seconds

            if target:
                target.current_hp -= ability.damage

            ability.last_used = time.time()

            return ability.damage

        else:
            print(f"Could not use {ability_name}!")
            return -1

    def apply_cc(self, cc_type: str, duration: float):
        self.cc_effects[cc_type] = duration
        if cc_type == "snare":
            self.speed = self.base_speed / 2

    def update_cc(self, dt: float):
        for cc_type in self.cc_effects:
            if self.cc_effects[cc_type] > 0:
                self.cc_effects[cc_type] -= dt
                if self.cc_effects[cc_type] <= 0:
                    self.cc_effects[cc_type] = 0
                    if cc_type == "snare":
                        self.speed = self.base_speed  # Restore speed

    def can_use(self, ability_name: str) -> bool:
        if ability_name not in self.abilities:
            print(f"Unable to use unknown ability: {ability_name}")
            return False

        return self.abilities.get(ability_name).can_use(time.time())
