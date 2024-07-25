from typing import List
from istate import IState
from iunit import IUnit


class GameState(IState):
    def __init__(self):
        self._units: List[IUnit] = []

    @property
    def units(self) -> List[IUnit]:
        return self._units

    def add_unit(self, unit: IUnit) -> None:
        self._units.append(unit)

    def update(self, dt: float) -> None:
        for unit in self.units:
            unit.update_auras(self)
