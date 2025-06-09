import random

import pygame

from settings import *


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, side):
        super().__init__()
        self.color = color
        self.height = 100
        self.width = 20
        self.side = side
        self.pos = ([20, SCREEN_HEIGHT // 2 - self.height // 2] if self.side == "left"
                    else [SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - self.height // 2])  # I have no idea why it is 40
        # initial pos

        self.display_surf = pygame.display.get_surface()

        self.helper_dict = {"left": {"up": pygame.K_w, "down": pygame.K_s},
                            "right": {"up": pygame.K_UP, "down": pygame.K_DOWN}}

        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.speed = 25

    def render(self):
        pygame.draw.rect(self.display_surf, self.color, self.rect, 20)
        # pygame.draw.rect(self.display_surf, "white", self.rect, 1)  # testing

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
            self.pos[1] = - self.height // 2 - 5  # -5 to avoid a conflict
            self.rect.y = self.pos[1]


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, paddles_group):
        super().__init__()
        self.color = color
        self.init_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.radius = 15

        self.display_surf = pygame.display.get_surface()

        self.movement = pygame.Vector2()
        self.speed = 5

        self.rect = pygame.rect.Rect(self.pos[0] - self.radius, self.pos[1], self.radius * 2, self.radius * 2)

        self.paddles_group = paddles_group

    def render(self):
        pygame.draw.circle(self.display_surf, self.color, self.pos, self.radius)
        pygame.draw.rect(self.display_surf, "yellow", self.rect, 1)  # testing

    def check_collision(self):  # it causes many illusions. Needs some improvements
        for paddle in self.paddles_group.sprites():
            collision_rect = (paddle.rect.left if paddle.side == "right" else paddle.rect.right
                              , paddle.rect.top, 1, paddle.height)
            top = (paddle.rect.left, paddle.rect.top, paddle.width, 1)
            bottom = (paddle.rect.left, paddle.rect.bottom, paddle.width, 1)
            pygame.draw.rect(self.display_surf, "yellow", collision_rect, 1)  # testing
            # pygame.draw.rect(self.display_surf, "orange", top, 1)  # testing
            # pygame.draw.rect(self.display_surf, "orange", bottom, 1)  # testing
            if self.rect.colliderect(top) or self.rect.colliderect(bottom):
                self.movement.y *= -1
            elif self.rect.colliderect(collision_rect):
                self.movement.x *= -1

    def check_edges(self, scores):
        if self.pos[0] <= self.radius // 2:
            self.pos = list(self.init_pos)
            self.movement.x *= -1
            self.movement.y = random.choice([-1, 1])
            scores['player 2'] += 1
        elif self.pos[0] >= SCREEN_WIDTH - self.radius // 2:
            self.pos = list(self.init_pos)
            self.movement.x *= -1
            self.movement.y = random.choice([-1, 1])
            scores['player 1'] += 1

    def move(self, dt):
        if not self.movement:
            self.movement.x = random.choice([-1, 1])
            self.movement.y = random.choice([-1, 1])

        self.pos[0] += self.movement.x * self.speed * dt
        self.pos[1] += self.movement.y * self.speed * dt

        # move the collision rect with the ball
        self.rect.x, self.rect.y = self.pos[0] - self.radius, self.pos[1] - self.radius
        # to place it in the center - self.radius

        if self.pos[1] <= self.radius or self.pos[1] >= SCREEN_HEIGHT - self.radius:
            self.movement.y *= -1

        self.check_collision()
