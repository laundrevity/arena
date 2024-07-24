import pygame as pg

from unit import Unit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)


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
            # Convert float positions to integers for drawing
            pos_int = [int(coord) for coord in unit.pos]
            color = BLUE if unit.player else RED
            pg.draw.circle(self.screen, color, pos_int, unit.radius)

            # Draw health bar
            self.draw_bar(unit, unit.current_hp / unit.max_hp, GREEN, -25)

            # Draw cast bar if casting
            if unit.casting_ability and not unit.casting_ability.is_instant:
                self.draw_bar(
                    unit,
                    unit.casting_ability.cast_time_elapsed
                    / unit.casting_ability.cast_time,
                    PURPLE,
                    25,
                )

            # Draw projectiles if exist
            for projectile in unit.projectiles:
                projectile.draw(self.screen)

        if paused:
            self.draw_text("PAUSED", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pg.display.flip()

    def draw_bar(self, unit: Unit, fill_ratio: float, color: tuple, offset_y: int):
        bar_width = unit.radius * 2
        bar_height = 5
        bar_bg_color = WHITE

        # Position the bar
        bar_x = int(unit.pos[0] - unit.radius)
        bar_y = int(unit.pos[1] + offset_y)

        # Draw the background of the bar
        pg.draw.rect(self.screen, bar_bg_color, (bar_x, bar_y, bar_width, bar_height))

        # Draw the foreground of the bar
        pg.draw.rect(
            self.screen, color, (bar_x, bar_y, int(bar_width * fill_ratio), bar_height)
        )

    def draw_text(self, text: str, x: int, y: int):
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
