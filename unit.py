class Unit:
    pos: list[int]
    player: bool
    radius: int
    speed: int

    def __init__(self, player: bool, initial_pos: list[int]):
        self.pos = initial_pos
        self.player = player
        self.radius = 20
        self.speed = 5
