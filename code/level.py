import pygame

from components import Paddle, Ball
from score import Score
from colors import get_color


class Level:
    def __init__(self, colors: dict):
        self.colors = colors

        self.right_paddle = Paddle(get_color(self.colors, 'paddle 1'), "right")
        self.left_paddle = Paddle(get_color(self.colors, 'paddle 2'), "left")
        # noinspection PyTypeChecker
        self.paddles_group = pygame.sprite.Group(self.right_paddle, self.left_paddle)
        self.ball = Ball(get_color(self.colors, 'ball'), self.paddles_group)

        self.scores = {'player 1': 0, 'player 2': 0}
        self.score = Score(self.scores, (get_color(self.colors, 'paddle 1'),
                                         get_color(self.colors, 'paddle 2')))

    def re_init(self):
        self.ball.color = get_color(self.colors, 'ball')
        self.right_paddle.color = get_color(self.colors, 'paddle 1')
        self.left_paddle.color = get_color(self.colors, 'paddle 2')
        self.score.paddle_colors = (get_color(self.colors, 'paddle 1'), get_color(self.colors, 'paddle 2'))

    def reset(self):
        self.scores = {'player 1': 0, 'player 2': 0}
        self.right_paddle = Paddle(get_color(self.colors, 'paddle 1'), "right")
        self.left_paddle = Paddle(get_color(self.colors, 'paddle 2'), "left")
        self.ball = Ball(get_color(self.colors, 'ball'), self.paddles_group)

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
