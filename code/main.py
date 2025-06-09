import sys

import pygame

from settings import *
from level import Level
from start_screen import StartScreen

AII_COLORS = {
    'screen': {'colors': ['black', 'white'], 'pos': 0},
    'paddle 1': {'colors': ['red', 'blue', 'yellow', 'orange', 'green', 'purple'], 'pos': 0},
    'paddle 2': {'colors': ['blue', 'yellow', 'orange', 'green', 'purple', 'red'], 'pos': 0},
    'ball': {'colors': ['white', 'black', 'red', 'blue', 'yellow', 'orange', 'green', 'purple', 'dark gray'], 'pos': 0},
    'text': {'colors': ['white', 'black'], 'pos': 0},
    'button': {'colors': ['white', 'black'], 'pos': 0},
    'button text': {'colors': ['black', 'white'], 'pos': 0},
    'box': {'colors': ['yellow'], 'pos': 0}  # yellow temp
}
# Note: the paddles colors are the same except that the pos of colors of one is higher than the other by 1


class Game:
    def __init__(self):
        pygame.init()

        # Screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ping Pong by MXD")

        self.colors = AII_COLORS

        self.clock = pygame.time.Clock()
        self.level = Level(self.colors)

        self.start_screen = StartScreen(self.colors)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.colors['screen']['colors'][self.colors['screen']['pos']])
            # this one is also to delete the traces

            dt = self.clock.tick(FPS) / 100

            if self.start_screen.play_button.pressed:
                self.level.colors = self.colors
                pygame.mouse.set_visible(False)
                self.level.re_init()  # I couldn't figur out a way to call it only when I need it.
                self.level.run(dt)

                if pygame.key.get_pressed()[pygame.K_k]:
                    self.start_screen.play_button.pressed = False
                    pygame.mouse.set_visible(True)
                    self.level.reset()

            else:
                if not self.start_screen.settings_button.pressed:
                    self.start_screen.play_button.check_pressed()
                self.start_screen.update()
                self.colors = self.start_screen.colors

            # Update the game
            pygame.display.update()


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
