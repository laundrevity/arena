from agent import Agent


class AIAgent(Agent):
    def __init__(self, unit):
        super().__init__(unit)

    def choose_action(self, game_state):
        # Example naive AI logic (behavior tree)
        actions = []

        if self.unit.role == "melee":
            if self.unit.target and self.unit.distance_to_target(self.unit.target):
                actions.append("move_towards_target")
            else:
                actions.append("melee_attack")

        elif self.unit.role == "caster":
            if self.unit.casting_ability is None:
                for spell_name in ["magic_missile", "stun", "root", "snare"]:
                    if self.unit.can_use(spell_name):
                        actions.append(f"cast_{spell_name}")

        return actions
