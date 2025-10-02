import pygame

from ai import SmartPaddle
from settings import SCREEN_HEIGHT, SCREEN_WIDTH  # ,MODE, DEV
from components import Paddle, Ball
from score import Score
from colors import get_color
from sounds import play_sound


class Level:
    def __init__(self, colors: dict):
        self.display_surf = pygame.display.get_surface()
        self.colors = colors

        # Flags
        self.two_players = False

        self.paddles = {"ai": SmartPaddle(get_color('paddle 2')),
                        "normal": Paddle(get_color('paddle 2'), "right")}

        self.right_paddle = (self.paddles["ai"] if not self.two_players else self.paddles["normal"])
        self.left_paddle = Paddle(get_color('paddle 1'), "left")
        # noinspection PyTypeChecker
        self.paddles_group = pygame.sprite.Group(self.right_paddle, self.left_paddle)
        self.ball = Ball(get_color('ball'))

        self.scores = {'player 1': 0, 'player 2': 0}
        self.score = Score(self.scores, (get_color('paddle 1'),
                                         get_color('paddle 2')),
                           ("Player", "Computer") if not self.two_players else (None, None))

        if not self.two_players:
            self.right_paddle.get_ball(self.ball)

    def re_init(self):
        self.right_paddle.change_color((self.paddles["ai"] if not self.two_players else self.paddles["normal"]))
        self.ball.change_color(get_color('ball'))
        self.right_paddle.change_color(get_color('paddle 2'))
        self.left_paddle.change_color(get_color('paddle 1'))
        self.score.paddle_colors = (get_color('paddle 1'), get_color('paddle 2'))
        self.score.get_names(("Player", "Computer") if not self.two_players else (None, None))

        self.paddles_group.empty()
        # noinspection PyTypeChecker
        self.paddles_group.add(self.right_paddle, self.left_paddle)

    def get_right_paddle(self):
        self.paddles = {"ai": SmartPaddle(get_color('paddle 2')),
                        "normal": Paddle(get_color('paddle 2'), "right")}

        self.right_paddle = (self.paddles["ai"] if not self.two_players else self.paddles["normal"])

        if not self.two_players:
            self.right_paddle.get_ball(self.ball)

    def reset(self):
        self.scores = {'player 1': 0, 'player 2': 0}
        self.left_paddle.reset()

        self.paddles_group.empty()
        # noinspection PyTypeChecker
        self.paddles_group.add(self.right_paddle, self.left_paddle)

        self.ball.reset()
        self.get_right_paddle()

    def check_collision(self):
        # Ball \ Paddle collisions
        for paddle in self.paddles_group.sprites():
            collision_rect = (paddle.rect.left if paddle.side == "right" else paddle.rect.right,
                              paddle.rect.top, 1, paddle.height)
            top = (paddle.rect.left + 1, paddle.rect.top, paddle.width - 1, 1)
            bottom = (paddle.rect.left + 1, paddle.rect.bottom - 1, paddle.width - 1, 1)

            if self.ball.rect.colliderect(top) and self.ball.movement.y == 1:
                self.ball.movement.y *= -1
                play_sound('hit')
            elif self.ball.rect.colliderect(bottom) and self.ball.movement.y == -1:
                self.ball.movement.y *= -1
                play_sound('hit')
            elif self.ball.rect.colliderect(collision_rect):
                if (paddle.side == "left" and self.ball.movement.x == -1 or
                        paddle.side == "right" and self.ball.movement.x == 1):
                    self.ball.movement.x *= -1
                    play_sound('hit')

    def draw_components(self):
        self.draw_board()
        self.right_paddle.draw()
        self.left_paddle.draw()
        self.ball.draw()
        self.score.display()

    def draw_board(self):
        # Middle
        pygame.draw.line(self.display_surf, get_color('line'),
                         (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        pygame.draw.rect(self.display_surf, get_color('line'),
                         (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50), 1)

        # Boarders
        pygame.draw.line(self.display_surf, get_color('line'),
                         (0, 1), (SCREEN_WIDTH, 1))
        pygame.draw.line(self.display_surf, get_color('line'),
                         (0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH, SCREEN_HEIGHT - 1))
        pygame.draw.line(self.display_surf, get_color('line'),
                         (1, 0), (1, SCREEN_HEIGHT))
        pygame.draw.line(self.display_surf, get_color('line'),
                         (SCREEN_WIDTH - 2, 0), (SCREEN_WIDTH - 2, SCREEN_HEIGHT))

    def move_components(self, dt):
        self.right_paddle.move(dt)
        self.left_paddle.move(dt)
        self.ball.move(dt)

    def run(self, dt):
        self.check_collision()
        self.ball.check_edges(self.scores)
        self.move_components(dt)
        self.score.update_score(self.scores)
        self.draw_components()
