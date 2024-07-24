import argparse
import logging

from game import Game
from logger_setup import setup_logger


def main():
    parser = argparse.ArgumentParser(description="Arena Game")
    parser.add_argument(
        "--debug",
        type=str,
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--bt",
        type=int,
        default=1,
        help="Set the battle type (1: Human vs AI, 2: AI vs AI)`",
    )
    parser.add_argument(
        "--p1",
        type=int,
        default=1,
        help="Set the player1 role (1: Caster, 2: Melee)`",
    )
    parser.add_argument(
        "--p2",
        type=int,
        default=2,
        help="Set the player2 role (1: Caster, 2: Melee)`",
    )

    args = parser.parse_args()

    # Convert logging level from string to logging constant
    log_level = getattr(logging, args.debug.upper(), logging.INFO)
    logger = setup_logger("arena_game", log_level)
    logger.info("Starting the game...")

    battle_config = {
        "battle_type": args.bt,
        "player_role": args.p1,
        "ai_role": args.p2,
    }

    g = Game(logger, config=battle_config)
    g.run()
    logger.info("Game has ended.")


if __name__ == "__main__":
    main()
