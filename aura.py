from iaura import IAura
from istate import IState
from iunit import IUnit


class Aura(IAura):
    def __init__(self, name: str, duration: float, positive: bool, effect):
        self._name = name
        self._duration = duration
        self._positive = positive
        self._effect = effect
        self._time_left = duration

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def positive(self) -> bool:
        return self._positive

    def apply(self, state: IState, unit: IUnit) -> None:
        self._effect(state, unit)

    def remove(self, state: IState, unit: IUnit) -> None:
        # Define what happens when the aura is removed
        pass

    def tick(self, state: IState, unit: IUnit) -> None:
        self._time_left -= 1
        if self._time_left <= 0:
            self.remove(state, unit)
        else:
            self._effect(state, unit)
