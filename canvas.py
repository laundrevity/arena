import pygame as pg

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Canvas:
    screen: pg.Surface

    def __init__(self, caption: str = "arena"):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(caption)

    def draw(self):
        self.screen.fill(WHITE)
        pg.display.flip()
