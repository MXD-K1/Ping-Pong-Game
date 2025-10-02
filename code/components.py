import random
from abc import ABC, abstractmethod

import pygame

from settings import *
from sounds import play_sound


class GameComponent(pygame.sprite.Sprite, ABC):
    def __init__(self, color):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.color = color
        self.rect = None

    @abstractmethod
    def draw(self): pass

    @abstractmethod
    def move(self, dt): pass

    @abstractmethod
    def reset(self): pass

    def change_color(self, color):
        self.color = color


class Paddle(GameComponent):
    def __init__(self, color, side: Literal["left", "right"]):
        super().__init__(color)

        self.height = 100
        self.width = 20
        self.side = side

        # initial pos
        self._init_pos = ((20, SCREEN_HEIGHT // 2 - self.height // 2) if self.side == "left"
                          else (SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - self.height // 2))
        # 40 = 20 the margin + 20 the paddle width

        self.pos = list(self._init_pos)

        self.display_surf = pygame.display.get_surface()

        self.helper_dict = {"left": {"up": pygame.K_w, "down": pygame.K_s},
                            "right": {"up": pygame.K_UP, "down": pygame.K_DOWN}}

        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.speed = 20

    def draw(self):
        pygame.draw.rect(self.display_surf, self.color, self.rect)

    def move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[self.helper_dict[self.side]["up"]]:
            self.pos[1] -= self.speed * dt
        if keys[self.helper_dict[self.side]["down"]]:
            self.pos[1] += self.speed * dt

        self.rect.y = self.pos[1]

        if self.rect.y <= - self.height // 2:
            self.pos[1] = SCREEN_HEIGHT - self.height // 2 - 5  # -5 to avoid a conflict
            self.rect.y = self.pos[1]
        elif self.rect.y >= SCREEN_HEIGHT - self.height // 2:
            self.pos[1] = - self.height // 2 + 5  # +5 to avoid a conflict
            self.rect.y = self.pos[1]

    def reset(self):
        self.pos = list(self._init_pos)
        self.rect.x, self.rect.y = self.pos


class Ball(GameComponent):
    def __init__(self, color):
        super().__init__(color)
        self.init_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.radius = 15

        self.movement = pygame.Vector2()
        self.speed = 20

        self.rect = pygame.rect.Rect(self.pos[0] - self.radius, self.pos[1], self.radius * 2, self.radius * 2)

    def draw(self):
        pygame.draw.circle(self.display_surf, self.color, self.pos, self.radius)

    def check_edges(self, scores):
        if self.pos[0] <= self.radius // 2:
            self.pos = list(self.init_pos)
            self.movement.x *= -1
            self.movement.y = random.choice([-1, 1])
            scores['player 2'] += 1
            play_sound('score')
        elif self.pos[0] >= SCREEN_WIDTH - self.radius // 2:
            self.pos = list(self.init_pos)
            self.movement.x *= -1
            self.movement.y = random.choice([-1, 1])
            scores['player 1'] += 1
            play_sound('score')

        # Check upper and lower edges
        if self.pos[1] <= self.radius and self.movement.y == -1:
            self.movement.y *= -1
            play_sound('hit')
        elif self.pos[1] >= SCREEN_HEIGHT - self.radius and self.movement.y == 1:
            self.movement.y *= -1
            play_sound('hit')

    def move(self, dt):
        if not self.movement.magnitude():
            self.movement.x = random.choice([-1, 1])
            self.movement.y = random.choice([-1, 1])

        self.pos[0] += self.movement.x * self.speed * dt
        self.pos[1] += self.movement.y * self.speed * dt

        # move the collision rect with the ball
        self.rect.x, self.rect.y = self.pos[0] - self.radius, self.pos[1] - self.radius
        # to place it in the center - self.radius

    def reset(self):
        self.pos = list(self.init_pos)
        self.rect.x, self.rect.y = self.pos
