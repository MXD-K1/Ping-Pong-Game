import pygame

from components import Paddle, Ball
from score import Score


class Level:
    def __init__(self, colors: dict):
        self.colors = colors
        self.right_paddle = Paddle(self.colors['paddle 1']['colors'][self.colors['paddle 1']['pos']], "right")
        self.left_paddle = Paddle(self.colors['paddle 2']['colors'][self.colors['paddle 2']['pos']], "left")

        # noinspection PyTypeChecker
        self.paddles_group = pygame.sprite.Group(self.right_paddle, self.left_paddle)

        self.ball = Ball(self.colors['ball']['colors'][self.colors['ball']['pos']], self.paddles_group)
        self.scores = {'player 1': 0, 'player 2': 0}
        self.score = Score(self.scores, (self.colors['paddle 1']['colors'][self.colors['paddle 1']['pos']],
                                         self.colors['paddle 2']['colors'][self.colors['paddle 2']['pos']]))

    def re_init(self):
        self.ball.color = self.colors['ball']['colors'][self.colors['ball']['pos']]
        self.right_paddle.color = self.colors['paddle 1']['colors'][self.colors['paddle 1']['pos']]
        self.left_paddle.color = self.colors['paddle 2']['colors'][self.colors['paddle 2']['pos']]
        self.score.paddle_colors = (self.colors['paddle 1']['colors'][self.colors['paddle 1']['pos']],
                                    self.colors['paddle 2']['colors'][self.colors['paddle 2']['pos']])

    def reset(self):
        self.scores = {'player 1': 0, 'player 2': 0}
        self.right_paddle = Paddle(self.colors['paddle 1']['colors'][self.colors['paddle 1']['pos']], "right")
        self.left_paddle = Paddle(self.colors['paddle 2']['colors'][self.colors['paddle 2']['pos']], "left")
        self.ball = Ball(self.colors['ball']['colors'][self.colors['ball']['pos']], self.paddles_group)

    def display_components(self, dt):
        self.right_paddle.move(dt)
        self.left_paddle.move(dt)
        self.right_paddle.render()
        self.left_paddle.render()
        self.ball.move(dt)
        self.ball.check_edges(self.scores)
        self.ball.render()

    def run(self, dt):
        self.display_components(dt)
        self.score.update_scores(self.scores)
        self.score.display()
