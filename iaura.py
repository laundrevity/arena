from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from istate import IState
    from iunit import IUnit


class IAura(ABC):
    @abstractmethod
    def apply(self, state: "IState", unit: "IUnit") -> None:
        pass

    @abstractmethod
    def remove(self, state: "IState", unit: "IUnit") -> None:
        pass

    @abstractmethod
    def tick(self, state: "IState", unit: "IUnit") -> None:
        pass

    @property
    @abstractmethod
    def duration(self) -> float:
        pass

    @property
    @abstractmethod
    def positive(self) -> bool:
        pass
