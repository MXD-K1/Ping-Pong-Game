import sys

import pygame

from settings import *
from level import Level
from start_screen import StartScreen, Label

ALL_COLORS = {
    'screen': {'colors': ['black', 'white'], 'pos': 0},
    'paddle 1': {'colors': ['red', 'blue', 'yellow', 'orange', 'green', 'purple', 'cyan'], 'pos': 0},
    'paddle 2': {'colors': ['blue', 'yellow', 'orange', 'green', 'purple', 'cyan', 'red'], 'pos': 0},
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

        self.level_initialized = False  # To init the game only when needed

    def get_color(self, key):
        return self.colors[key]['colors'][self.colors[key]['pos']]

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        if self.start_screen.play_button.pressed:
            if not self.level_initialized:
                self.level.colors = self.colors
                pygame.mouse.set_visible(False)
                self.level.re_init()
                self.level_initialized = True

            if pygame.key.get_pressed()[pygame.K_k]:
                self.start_screen.play_button.pressed = False
                pygame.mouse.set_visible(True)
                self.level.reset()
                self.level_initialized = False

        else:
            if not self.start_screen.settings_button.pressed:
                self.start_screen.play_button.check_pressed()

            self.colors = self.start_screen.colors

    def draw(self, dt, fps_label):
        self.screen.fill(self.get_color('screen'))

        if self.start_screen.play_button.pressed:
            self.level.run(dt)
        else:
            self.start_screen.update()

        fps_label.draw()
        pygame.display.update()

    def run(self):
        fps_label = Label(self.screen, "", self.get_color('text'),
                          (50, SCREEN_HEIGHT - 20), 24)
        while True:
            self.handle_events()

            dt = self.clock.tick(FPS) / 100
            fps_label.text = f"FPS: {self.clock.get_fps():.2f}"

            self.update()
            self.draw(dt, fps_label)


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
