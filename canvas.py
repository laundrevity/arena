import pygame as pg

from unit import Unit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Canvas:
    screen: pg.Surface
    font: pg.font.Font

    def __init__(self, caption: str = "arena"):
        pg.font.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(caption)
        self.font = pg.font.SysFont(None, 48)  # Initialize font

    def draw(self, units: list[Unit] = [], paused: bool = False):
        self.screen.fill(WHITE)

        for unit in units:
            # NOTE: assuming here that Unit has these methods! maybe make them abstract?
            # Convert float positions to integers for drawing
            pos_int = [int(coord) for coord in unit.pos]
            color = BLUE if unit.player else RED
            pg.draw.circle(self.screen, color, pos_int, unit.radius)

        if paused:
            self.draw_text("PAUSED", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pg.display.flip()

    def draw_text(self, text: str, x: int, y: int):
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
