# import random

from settings import *
from components import Paddle


class SmartPaddle(Paddle):
    def __init__(self, color):
        super().__init__(color, "right")
        self.ball = None
        # self.speed *= 0.75  # when increased to more than 1, it causes some weird moving animation

    def get_ball(self, ball):
        self.ball = ball

    def move(self, dt):
        if self.ball.movement.x == 1:
            if self.ball.pos[1] > self.pos[1] + self.height // 2:
                self.pos[1] += self.speed * dt
            elif self.ball.pos[1] < self.pos[1]:
                self.pos[1] -= self.speed * dt

            # a very small random chance that AI will make a mistake
            """if random.randint(0, 1000) < 20:  # didn't work as expected
                self.pos[1] += self.speed * dt * self.ball.movement.y * 5"""

        self.rect.y = self.pos[1]  # move the paddle

        if self.rect.y <= - self.height // 2:
            self.pos[1] = SCREEN_HEIGHT - self.height // 2 - 5
            self.rect.y = self.pos[1]
        elif self.rect.y >= SCREEN_HEIGHT - self.height // 2:
            self.pos[1] = - self.height // 2 - 5
            self.rect.y = self.pos[1]
