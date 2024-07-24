from game import Game
from logger_setup import setup_logger


def main():
    logger = setup_logger("arena_game")
    logger.info("Starting the game...")
    g = Game(logger)
    g.run()
    logger.info("Game has ended.")


if __name__ == "__main__":
    main()
