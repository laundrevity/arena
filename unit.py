import math


class Unit:
    pos: list[float]
    player: bool
    radius: int
    speed: int

    def __init__(self, player: bool, initial_pos: list[float]):
        self.pos = initial_pos
        self.player = player
        self.radius = 20
        self.speed = 100  # Adjust for reasonable movement

    def move(self, direction: list[float], dt: float) -> None:
        norm = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if norm != 0:
            direction[0] /= norm
            direction[1] /= norm

        dx = direction[0] * self.speed * dt
        dy = direction[1] * self.speed * dt

        self.pos[0] += dx
        self.pos[1] += dy
