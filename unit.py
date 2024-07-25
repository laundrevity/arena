from typing import List
from iunit import IUnit
from iability import IAbility
from iaura import IAura
from istate import IState


class Unit(IUnit):
    def __init__(self, uid: int, hp: int):
        self._uid = uid
        self._hp = hp
        self._abilities: List[IAbility] = []
        self._auras: List[IAura] = []

    @property
    def abilities(self) -> List[IAbility]:
        return self._abilities

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = value

    @property
    def uid(self) -> int:
        return self._uid

    @property
    def auras(self) -> List[IAura]:
        return self._auras

    def add_ability(self, ability: IAbility) -> None:
        self._abilities.append(ability)

    def add_aura(self, aura: IAura, state: IState) -> None:
        self._auras.append(aura)
        aura.apply(state, self)

    def update_auras(self, state: IState) -> None:
        for aura in self._auras:
            aura.tick(state, self)
