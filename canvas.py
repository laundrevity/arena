import time

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
DULL_GRAY = (169, 169, 169)


class Canvas:
    screen: pg.Surface
    font: pg.font.Font

    def __init__(self, caption: str = "arena"):
        pg.font.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(caption)
        self.font = pg.font.SysFont(None, 48)  # Initialize font
        self.icon_font = pg.font.SysFont(None, 24)  # Font for hotkeys

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

        self.draw_ability_cooldowns(units[0])  # Draw player ability cooldowns

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

    def draw_ability_cooldowns(self, unit: Unit):
        current_time = time.time()
        x, y = 50, SCREEN_HEIGHT - 150  # Starting position for cooldown icons

        idx = 0
        for ability_name, ability in unit.abilities.items():
            if ability.cooldown > 0 and "melee" not in ability_name:
                cd_left = max(0, ability.cooldown - (current_time - ability.last_used))
                icon_color = ability.color if cd_left == 0 else DULL_GRAY

                # Draw ability icon (square for simplicity)
                pg.draw.rect(self.screen, icon_color, (x, y, 40, 40))
                pg.draw.rect(self.screen, BLACK, (x, y, 40, 40), 2)  # Border

                if unit.casting_ability and unit.casting_ability.name == ability_name:
                    # Show remaining cast time
                    cast_time_left = max(
                        0,
                        unit.casting_ability.cast_time
                        - unit.casting_ability.cast_time_elapsed,
                    )
                    text_surface = self.icon_font.render(cast_time_left, True, BLACK)
                    text_rect = text_surface.get_rect(center=(x + 20, y + 20))
                    self.screen.blit(text_surface, text_rect)
                elif cd_left > 0:
                    # Draw cooldown time
                    text_surface = self.icon_font.render(f"{cd_left:.1f}", True, BLACK)
                    text_rect = text_surface.get_rect(center=(x + 20, y + 20))
                    self.screen.blit(text_surface, text_rect)
                else:
                    # Draw hotkey (assuming they like 1, 2, 3 etc)
                    hotkey = str(idx + 1)
                    text_surface = self.icon_font.render(hotkey, True, BLACK)
                    text_rect = text_surface.get_rect(center=(x + 20, y + 20))
                    self.screen.blit(text_surface, text_rect)

                x += 50  # Move to next position
                idx += 1
