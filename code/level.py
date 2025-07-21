import pygame

from ai import SmartPaddle
from settings import SCREEN_HEIGHT, SCREEN_WIDTH  # ,MODE, DEV
from components import Paddle, Ball
from score import Score
from colors import get_color


class Level:
    def __init__(self, colors: dict):
        self.display_surf = pygame.display.get_surface()
        self.colors = colors

        self.two_players = False

        self.paddles = {"ai": SmartPaddle(get_color(self.colors, 'paddle 2')),
                        "normal": Paddle(get_color(self.colors, 'paddle 2'), "right")}

        self.right_paddle = (self.paddles["ai"] if not self.two_players else self.paddles["normal"])
        self.left_paddle = Paddle(get_color(self.colors, 'paddle 1'), "left")
        # noinspection PyTypeChecker
        self.paddles_group = pygame.sprite.Group(self.right_paddle, self.left_paddle)
        self.ball = Ball(get_color(self.colors, 'ball'), self.paddles_group)

        self.scores = {'player 1': 0, 'player 2': 0}
        self.score = Score(self.scores, (get_color(self.colors, 'paddle 1'),
                           get_color(self.colors, 'paddle 2')),
                           ("Player", "Computer") if not self.two_players else (None, None))

        if not self.two_players:
            self.right_paddle.get_ball(self.ball)

    def re_init(self):
        self.right_paddle = (self.paddles["ai"] if not self.two_players else self.paddles["normal"])
        self.ball.color = get_color(self.colors, 'ball')
        self.right_paddle.color = get_color(self.colors, 'paddle 2')
        self.left_paddle.color = get_color(self.colors, 'paddle 1')
        self.score.paddle_colors = (get_color(self.colors, 'paddle 1'), get_color(self.colors, 'paddle 2'))
        self.score.names = ("Player", "Computer") if not self.two_players else ("Player 1", "Player 2")

        self.paddles_group.empty()
        # noinspection PyTypeChecker
        self.paddles_group.add(self.right_paddle, self.left_paddle)

    def reset(self):
        self.scores = {'player 1': 0, 'player 2': 0}
        self.right_paddle = Paddle(get_color(self.colors, 'paddle 1'), "right")
        self.left_paddle = Paddle(get_color(self.colors, 'paddle 2'), "left")

        self.paddles_group.empty()
        # noinspection PyTypeChecker
        self.paddles_group.add(self.right_paddle, self.left_paddle)

        self.ball = Ball(get_color(self.colors, 'ball'), self.paddles_group)

    def check_collision(self):  # it causes some illusions. Needs improvements
        for paddle in self.paddles_group.sprites():
            collision_rect = (paddle.rect.left if paddle.side == "right" else paddle.rect.right,
                              paddle.rect.top, 1, paddle.height)
            top = (paddle.rect.left + 1, paddle.rect.top, paddle.width - 1, 1)
            bottom = (paddle.rect.left + 1, paddle.rect.bottom - 1, paddle.width - 1, 1)

            """if MODE == DEV:
                pygame.draw.rect(self.display_surf, "white", collision_rect, 2)
                pygame.draw.rect(self.display_surf, "orange", top, 2)
                pygame.draw.rect(self.display_surf, "orange", bottom, 2)"""

            if self.ball.rect.colliderect(top) and self.ball.movement.y == 1:
                self.ball.movement.y *= -1
            elif self.ball.rect.colliderect(bottom) and self.ball.movement.y == -1:
                self.ball.movement.y *= -1
                self.ball.pos[1] += 3 * self.ball.movement.y
            elif self.ball.rect.colliderect(collision_rect):
                if (paddle.side == "left" and self.ball.movement.x == -1 or
                        paddle.side == "right" and self.ball.movement.x == 1):
                    self.ball.movement.x *= -1

    def display_components(self, dt):
        self.right_paddle.move(dt)
        self.left_paddle.move(dt)
        self.right_paddle.render()
        self.left_paddle.render()
        self.ball.move(dt)
        self.check_collision()
        self.ball.check_edges(self.scores)
        self.ball.render()
        self.draw_board()

    def draw_board(self):
        pygame.draw.line(self.display_surf, get_color(self.colors, 'line'),
                         (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        pygame.draw.rect(self.display_surf, get_color(self.colors, 'line'),
                         (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50), 1)

        # Boarders
        pygame.draw.line(self.display_surf, get_color(self.colors, 'line'),
                         (0, 1), (SCREEN_WIDTH, 1))
        pygame.draw.line(self.display_surf, get_color(self.colors, 'line'),
                         (0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH, SCREEN_HEIGHT - 1))
        pygame.draw.line(self.display_surf, get_color(self.colors, 'line'),
                         (1, 0), (1, SCREEN_HEIGHT))
        pygame.draw.line(self.display_surf, get_color(self.colors, 'line'),
                         (SCREEN_WIDTH - 1, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT))

    def run(self, dt):
        self.display_components(dt)
        self.score.update_scores(self.scores)
        self.score.display()
