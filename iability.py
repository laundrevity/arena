from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from istate import IState


class IAbility(ABC):
    @abstractmethod
    def __call__(self, state: "IState") -> None:
        pass
