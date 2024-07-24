import math


class Unit:
    pos: list[float]
    player: bool
    radius: int
    speed: int
    max_hp: int
    current_hp: int
    casting: bool
    cast_duration: float
    cast_time: float

    def __init__(self, player: bool, initial_pos: list[float], max_hp: int = 100):
        self.pos = initial_pos
        self.player = player
        self.radius = 20
        self.speed = 100  # Adjust for reasonable movement
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.casting = False
        self.cast_duration = 1
        self.cast_time = 0

    def move(self, direction: list[float], dt: float) -> None:
        norm = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if norm != 0:
            direction[0] /= norm
            direction[1] /= norm

        dx = direction[0] * self.speed * dt
        dy = direction[1] * self.speed * dt

        self.pos[0] += dx
        self.pos[1] += dy

        if self.casting:
            self.cancel_cast()

    def start_casting(self, duration: float):
        self.casting = True
        self.cast_duration = duration
        self.cast_time = 0

    def update_cast(self, dt: float):
        if self.casting:
            self.cast_time += dt
            if self.cast_time >= self.cast_duration:
                self.casting = False
                self.cast_time = 0
                return True  # indicate cast completion
        return False  # cast not completed

    def cancel_cast(self):
        self.casting = False
        self.cast_time = 0
