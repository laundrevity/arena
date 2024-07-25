from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from iunit import IUnit


class IState(ABC):
    @property
    @abstractmethod
    def units(self) -> List["IUnit"]:
        pass
