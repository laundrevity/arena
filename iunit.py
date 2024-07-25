from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from istate import IState
    from iability import IAbility
    from iaura import IAura


class IUnit(ABC):
    @property
    @abstractmethod
    def abilities(self) -> List["IAbility"]:
        pass

    @property
    @abstractmethod
    def hp(self) -> int:
        pass

    @hp.setter
    @abstractmethod
    def hp(self, value: int) -> None:
        pass

    @property
    @abstractmethod
    def uid(self) -> int:
        pass

    @property
    @abstractmethod
    def auras(self) -> List["IAura"]:
        pass

    @abstractmethod
    def add_ability(self, ability: "IAbility") -> None:
        pass

    @abstractmethod
    def add_aura(self, aura: "IAura", state: "IState") -> None:
        pass

    @abstractmethod
    def update_auras(self, state: "IState") -> None:
        pass
