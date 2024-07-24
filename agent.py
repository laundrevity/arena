from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, unit):
        self.unit = unit

    @abstractmethod
    def choose_action(self, game_state):
        pass
