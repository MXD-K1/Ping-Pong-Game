from typing import Literal

import pygame

from settings import  *


class Paddle:
    def __init__(self, color: str, side: Literal["right", "left"]):
        self.color = color
        self.height = 100
        self.width = 20
        self.side = side
        self.pos = ([20, SCREEN_HEIGHT // 2 - self.height // 2] if self.side == "left"
                    else [SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - self.height // 2])

        self.display_surf = pygame.display.get_surface()

        self.helper_dict = {"left": {"up": pygame.K_w, "down": pygame.K_s},
                            "right": {"up": pygame.K_UP, "down": pygame.K_DOWN}}

        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.speed = 20


    def render(self): ...

    def move(self, dt: int): ...


class Ball:
    def __init__(self, color, paddles_group):
        self.color = color
        self.init_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.radius = 15

        self.display_surf = pygame.display.get_surface()

        self.movement = pygame.Vector2()
        self.speed = 20

        self.rect = pygame.rect.Rect(*self.pos, self.radius, self.radius)

        self.paddles_group = paddles_group

    def render(self): ...

    def check_collision(self): ...

    def check_edges(self, scores): ...

    def move(self, dt: int): ...

