from abc import ABC, abstractmethod


class Action:
    def __init__(self, move_direction=None, ability_name=None):
        self.move_direction = move_direction  # [x, y] direction vector or None
        self.ability_name = ability_name  # Ability name or None


class Agent(ABC):
    def __init__(self, unit):
        self.unit = unit

    @abstractmethod
    def choose_action(self, game_state) -> Action: ...
