import sys

import pygame

from settings import *
from level import Level
from start_screen import StartScreen, Label
from colors import ALL_COLORS, get_color

from fonts import fonts


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

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, fps_label):
        start, players_num = self.start_screen.start_game()
        if start:
            if not self.level_initialized:
                self.level.reset()  # IF game is restarted by hitting k
                self.level.colors = self.colors
                pygame.mouse.set_visible(False)
                self.level.two_players = False if players_num == 1 else True
                self.level.re_init()
                self.start_screen.wait_timer.activate()
                self.level_initialized = True

            if pygame.key.get_pressed()[pygame.K_k]:
                self.start_screen.play_button.reset()
                self.start_screen.one_player_button.reset()
                self.start_screen.two_players_button.reset()
                pygame.mouse.set_visible(True)
                self.level.reset()
                self.start_screen.wait_timer.activate()
                self.level_initialized = False

            self.colors = self.start_screen.colors

        if MODE == DEV:
            fps_label.text = f"FPS: {self.clock.get_fps():.2f}"

    def draw(self, dt, fps_label):
        self.screen.fill(get_color('screen'))

        if self.start_screen.start_game()[0]:
            self.level.run(dt)
        else:
            self.start_screen.update()

        if MODE == DEV:
            fps_label.draw()
        pygame.display.update()

    def run(self):
        fps_label = Label("", get_color('text'),
                          (50, SCREEN_HEIGHT - 20), fonts['fps'])
        while True:
            self.handle_events()

            dt = self.clock.tick(FPS) / 100

            fps_label.color = get_color('text')
            self.update(fps_label)
            self.draw(dt, fps_label)


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
