from agent import Agent, Action


class AIAgent(Agent):
    def __init__(self, unit):
        super().__init__(unit)

    def choose_action(self, game_state):
        # Example naive AI logic (behavior tree)
        move_direction = [0, 0]
        ability_name = None

        if self.unit.role == "melee":
            if (
                self.unit.target
                and self.unit.distance_to_target(self.unit.target)
                > self.unit.abilities["melee_attack"].range
            ):
                move_direction = [
                    self.unit.target.pos[0] - self.unit.pos[0],
                    self.unit.target.pos[1] - self.unit.pos[1],
                ]
            else:
                ability_name = "melee_attack"

        elif self.unit.role == "caster":
            if self.unit.casting_ability is None:
                for spell_name in ["magic_missile", "stun", "root", "snare"]:
                    if self.unit.can_use(spell_name):
                        ability_name = f"cast_{spell_name}"
                        break

        self.unit.logger.debug(
            f"AI choose_action({game_state}) -> move: {move_direction}, ability: {ability_name}"
        )
        return Action(move_direction, ability_name)
