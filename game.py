from typing import Optional
import time

from battle import Battle
from canvas import Canvas


class Game:
    current_battle: Optional[Battle]
    canvas: Canvas
    debug: bool

    def __init__(self, debug: bool = False):
        self.current_battle = None
        self.canvas = Canvas()
        self.debug = debug

    def run(self):
        if self.current_battle is None:
            self.current_battle = self.setup_battle()

        if self.debug:
            print("starting new battle")

        last_time = time.time()

        while self.current_battle.is_active:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            self.current_battle.tick(dt)

            if self.current_battle.render:
                self.canvas.draw(self.current_battle.units, self.current_battle.paused)
        if self.debug:
            print("battle done")

    def setup_battle(self) -> Battle:
        print("Choose battle type:")
        print("1. Human vs AI")
        print("2. AI vs AI")
        battle_type = input("Enter 1 or 2: ")

        if battle_type not in ["1", "2"]:
            print("Invalid input. Defaulting to Human vs AI.")
            battle_type = "1"

        roles = ["caster", "melee"]
        if battle_type == "1":
            print("Choose your role: ")
            print("1. Caster")
            print("2. Melee")
            player_role = input("Enter 1 or 2:")
            if player_role not in ["1", "2"]:
                print("Invalid input. Defaulting to Caster.")
            player_role = roles[int(player_role) - 1]

            print("Chooise AI role:")
            print("1. Caster")
            print("2. Melee")
            ai_role = input("Enter 1 or 2:")
            if ai_role not in ["1", "2"]:
                print("Invalid input. Defaulting to Melee.")
            ai_role = roles[int(ai_role) - 1]

            return Battle(player_role=player_role, ai_role=ai_role, ai_vs_ai=False)

        elif battle_type == "2":
            print("Choose role for 1st AI: ")
            print("1. Caster")
            print("2. Melee")
            ai_role_1 = input("Enter 1 or 2:")
            if ai_role_1 not in ["1", "2"]:
                print("Invalid input. Defaulting to Caster.")
            ai_role_1 = roles[int(ai_role_1) - 1]

            print("Chooise role for 2nd AI:")
            print("1. Caster")
            print("2. Melee")
            ai_role_2 = input("Enter 1 or 2:")
            if ai_role_2 not in ["1", "2"]:
                print("Invalid input. Defaulting to Melee.")
            ai_role_2 = roles[int(ai_role_2) - 1]

            return Battle(
                player_role=None, ai_role=ai_role_1, ai2_role=ai_role_2, ai_vs_ai=True
            )

    def draw_debug_info(self):
        # Implement debug info display
        pass
