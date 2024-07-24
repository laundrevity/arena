from typing import Optional


class Ability:
    def __init__(
        self,
        name: str,
        cast_time: float,
        cooldown: float,
        damage: int,
        is_instant: bool,
        off_gcd: bool,
        color: tuple,
        range: float = 0,
        cc_type: Optional[str] = None,
    ):
        self.name = name
        self.cast_time = cast_time  # Cast time in seconds
        self.cooldown = cooldown  # Cooldown time in seconds
        self.damage = damage
        self.is_instant = is_instant
        self.off_gcd = off_gcd
        self.color = color
        self.last_used = -cooldown  # Timestamp of last use
        self.range = range
        self.cc_type = cc_type  # e.g., 'snare', 'root', 'stun'

    def can_use(self, current_time: float):
        return current_time - self.last_used >= self.cooldown

    def use(self, current_time: float):
        self.last_used = current_time
        return self.damage

    def is_on_cooldown(self, current_time: float):
        return current_time - self.last_used < self.cooldown


class Projectile:
    def __init__(
        self,
        start_pos: list[float],
        target_pos: list[float],
        color: tuple,
        speed: float = 300,
    ):
        self.pos = start_pos[:]
        self.target_pos = target_pos
        self.color = color
        self.radius = 5
        self.speed = speed

    def move(self, dt: float):
        direction = [self.target_pos[0] - self.pos[0], self.target_pos[1] - self.pos[1]]
        norm = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        if norm != 0:
            direction[0] /= norm
            direction[1] /= norm

        dx = direction[0] * self.speed * dt
        dy = direction[1] * self.speed * dt

        self.pos[0] += dx
        self.pos[1] += dy

    def draw(self, screen):
        import pygame as pg

        pg.draw.circle(
            screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius
        )
