

import sys
import pygame

from settings import *
from level import Level
from start_screen import StartScreen

# Fixed typo: AII_COLORS → ALL_COLORS
ALL_COLORS = {
    'screen': {'colors': ['black', 'white'], 'pos': 0},
    'paddle 1': {'colors': ['red', 'blue', 'yellow', 'orange', 'green', 'purple'], 'pos': 0},
    'paddle 2': {'colors': ['blue', 'yellow', 'orange', 'green', 'purple', 'red'], 'pos': 0},
    'ball': {'colors': ['white', 'black', 'red', 'blue', 'yellow', 'orange', 'green', 'purple', 'dark gray'], 'pos': 0},
    'text': {'colors': ['white', 'black'], 'pos': 0},
    'button': {'colors': ['white', 'black'], 'pos': 0},
    'button text': {'colors': ['black', 'white'], 'pos': 0},
    'box': {'colors': ['yellow'], 'pos': 0}  # yellow temp
}


class Game:
    def __init__(self):
        pygame.init()

        # Screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ping Pong by MXD")

        self.colors = ALL_COLORS
        self.clock = pygame.time.Clock()
        self.level = Level(self.colors)
        self.start_screen = StartScreen(self.colors)

        self.level_initialized = False

    def get_color(self, key):
        return self.colors[key]['colors'][self.colors[key]['pos']]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt):
        if self.start_screen.play_button.pressed:
            if not self.level_initialized:
                self.level.colors = self.colors
                pygame.mouse.set_visible(False)
                self.level.re_init()
                self.level_initialized = True

            self.level.run(dt)

            if pygame.key.get_pressed()[pygame.K_k]:
                self.start_screen.play_button.pressed = False
                pygame.mouse.set_visible(True)
                self.level.reset()
                self.level_initialized = False

        else:
            if not self.start_screen.settings_button.pressed:
                self.start_screen.play_button.check_pressed()
            self.start_screen.update()
            self.colors = self.start_screen.colors

    def draw(self):
        self.screen.fill(self.get_color('screen'))
        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()

            dt = self.clock.tick(FPS) / 100
            pygame.display.set_caption(f"Ping Pong by MXD - FPS: {self.clock.get_fps():.2f}")

            self.update(dt)
            self.draw()


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
