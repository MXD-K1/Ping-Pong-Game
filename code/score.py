import pygame

from settings import *


class Score:
    def __init__(self, scores, paddle_colors):
        self.scores = scores
        self.font = pygame.font.Font(None, 26)  # the default font will be used
        self.display_surf = pygame.display.get_surface()

        self.paddle_colors = paddle_colors

    def update_scores(self, scores):
        self.scores = scores

    def display(self):
        red_font = self.font.render(f'Player 2: {self.scores['player 2']}',
                                    True, self.paddle_colors[0])
        blue_font = self.font.render(f'Player 1: {self.scores['player 1']}',
                                     True, self.paddle_colors[1])
        self.display_surf.blit(blue_font, (SCREEN_WIDTH // 2 - 100, 20))
        self.display_surf.blit(red_font, (SCREEN_WIDTH // 2 + 20, 20))
