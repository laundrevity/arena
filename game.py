from typing import Optional
import time
from logging import Logger

from battle import Battle
from canvas import Canvas


class Game:
    current_battle: Optional[Battle]
    canvas: Canvas
    debug: bool
    logger: Logger
    config: dict

    def __init__(self, logger: Logger, config: dict = None):
        self.current_battle = None
        self.canvas = Canvas()
        self.logger = logger
        self.config = config

    def run(self):
        if self.current_battle is None:
            self.current_battle = self.setup_battle()

        self.logger.debug("starting new battle")

        last_time = time.time()

        while self.current_battle.is_active:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            self.current_battle.tick(dt)

            if self.current_battle.render:
                self.canvas.draw(self.current_battle.units, self.current_battle.paused)

        self.logger.debug("battle done")

    def setup_battle(self) -> Battle:
        if self.config:
            battle_type = self.config.get("battle_type", 1)
            player_role = self.config.get("player_role", 1)
            ai_role = self.config.get("ai_role", 2)

            roles = ["caster", "melee"]
            if battle_type == 1:
                return Battle(
                    self.logger,
                    player_role=roles[player_role - 1],
                    ai_role=roles[ai_role - 1],
                    ai_vs_ai=False,
                )
            elif battle_type == 2:
                return Battle(
                    self.logger,
                    player_role=None,
                    ai_role=roles[player_role - 1],
                    ai2_role=roles[ai_role - 1],
                    ai_vs_ai=True,
                )

        else:
            self.logger.error("Failed to find self.config so cannot setup battle!")

    def draw_debug_info(self):
        # Implement debug info display
        pass
