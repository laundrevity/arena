from iability import IAbility
from istate import IState


class Fireball(IAbility):
    def __init__(self, dmg: int, cast_time: float, src: int, dst: int):
        self.dmg = dmg
        self.cast_time = cast_time
        self.src = src
        self.dst = dst

    def __call__(self, state: IState) -> None:
        for unit in state.units:
            if unit.uid == self.dst:
                unit.hp -= self.dmg
