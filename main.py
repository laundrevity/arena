from state import GameState
from unit import Unit
from ability import Fireball
from aura import Aura


def main():
    game_state = GameState()

    unit1 = Unit(uid=1, hp=100)
    unit2 = Unit(uid=2, hp=100)

    fireball = Fireball(dmg=30, cast_time=1.0, src=1, dst=2)
    dot_aura = Aura(
        name="Burn",
        duration=5,
        positive=False,
        effect=lambda state, unit: setattr(unit, "hp", unit.hp - 5),
    )

    unit1.add_ability(fireball)
    game_state.add_unit(unit1)
    game_state.add_unit(unit2)

    unit2.add_aura(dot_aura, game_state)

    fireball(game_state)
    game_state.update(dt=1.0)

    for unit in game_state.units:
        print(f"Unit {unit.uid} HP: {unit.hp}")


if __name__ == "__main__":
    main()
