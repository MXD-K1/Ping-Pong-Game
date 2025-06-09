import time

import pygame

from settings import *


class StartScreen:
    def __init__(self, colors):
        self.colors = colors
        self.display_surf = pygame.display.get_surface()

        self.font = pygame.font.SysFont(None, 48)
        self.play_button = Button(self.display_surf, self.colors['button']['colors'][self.colors['button']['pos']],
                                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),
                                  "Play", 42,
                                  self.colors['button text']['colors'][self.colors['button text']['pos']])

        self.settings_button = Button(self.display_surf, self.colors['button']['colors'][self.colors['button']['pos']],
                                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                      "Settings", 32,
                                      self.colors['button text']['colors'][self.colors['button text']['pos']])

    def re_init(self):
        self.play_button.color = self.colors['button']['colors'][self.colors['button']['pos']]
        self.play_button.font_color = self.colors['button text']['colors'][self.colors['button text']['pos']]
        self.settings_button.color = self.colors['button']['colors'][self.colors['button']['pos']]
        self.settings_button.font_color = self.colors['button text']['colors'][self.colors['button text']['pos']]

    def update(self):
        self.settings_button.check_pressed()
        if self.settings_button.pressed:
            self.show_settings()
        else:
            self.play_button.display()
            self.settings_button.display()
            welcome_text = self.font.render("Welcome to Ping Pong", False,
                                            self.colors['text']['colors'][self.colors['text']['pos']])
            self.display_surf.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, 50))

    def show_settings(self):
        msg = self.font.render("Choose the mode color you want", False,
                               self.colors['text']['colors'][self.colors['text']['pos']])
        self.display_surf.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 50))

        return_button = Button(self.display_surf, self.colors['button']['colors'][self.colors['button']['pos']],
                               (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100),
                               "Return", 42,
                               self.colors['button text']['colors'][self.colors['button text']['pos']])

        color_choices = ['Screen', 'Paddle 1', 'Paddle 2', 'Ball']
        settings = []
        for index, choice in enumerate(color_choices, 1):
            setting_colors = {'button': self.colors['button']['colors'][self.colors['button']['pos']],
                              'box': self.colors['box']['colors'][self.colors['box']['pos']],
                              'text': self.colors['text']['colors'][self.colors['text']['pos']],
                              choice.lower(): self.colors[choice.lower()]['colors'][self.colors[choice.lower()]['pos']]
                              }

            settings.append(SettingChoice((SCREEN_HEIGHT - 450 + 50 * index), choice, setting_colors['button'],
                                          setting_colors['box'], setting_colors['text'],
                                          setting_colors[choice.lower()]))

        return_button.display()

        for setting in settings:
            setting.update()
            if setting.is_pressed() == "right":
                self.colors[setting.name.lower()]['pos'] -= 1

                if self.colors[setting.name.lower()]['pos'] < 0:
                    self.colors[setting.name.lower()]['pos'] = len(self.colors[setting.name.lower()]['colors']) - 1
                elif self.colors[setting.name.lower()]['pos'] > len(self.colors[setting.name.lower()]['colors']) - 1:
                    self.colors[setting.name.lower()]['pos'] = 0

                if setting.name.lower() == 'screen':
                    self.colors['text']['pos'] = self.colors['screen']['pos']
                    self.colors['button']['pos'] = self.colors['screen']['pos']
                    self.colors['button text']['pos'] = self.colors['screen']['pos']

                time.sleep(0.2)  # to add it once

            elif setting.is_pressed() == "left":
                self.colors[setting.name.lower()]['pos'] += 1

                if self.colors[setting.name.lower()]['pos'] < 0:
                    self.colors[setting.name.lower()]['pos'] = len(self.colors[setting.name.lower()]['colors']) - 1
                elif self.colors[setting.name.lower()]['pos'] > len(self.colors[setting.name.lower()]['colors']) - 1:
                    self.colors[setting.name.lower()]['pos'] = 0

                if setting.name.lower() == 'screen':
                    self.colors['text']['pos'] = self.colors['screen']['pos']
                    self.colors['button']['pos'] = self.colors['screen']['pos']
                    self.colors['button text']['pos'] = self.colors['screen']['pos']

                time.sleep(0.2)  # to add it once only

        return_button.check_pressed()
        if return_button.pressed:
            self.settings_button.pressed = False

        self.re_init()


class Button:
    def __init__(self, display_surface: pygame.Surface, color, pos: tuple[int, int],
                 text=None, font_size=None, font_color=None):
        self.color = color
        self.pos = pos
        self.display_surf = display_surface

        if text:
            self.text = text
            self.font = pygame.font.SysFont(None, font_size)
            self.font_color = font_color
            self.no_text = False
        else:
            self.no_text = True

        self.rect = pygame.rect.Rect(pos[0], pos[1], 100, 50)
        self.rect.x -= self.rect.width // 2
        self.rect.y -= self.rect.height // 2

        self.pressed = False

    def display(self):
        pygame.draw.rect(self.display_surf, self.color, self.rect, border_radius=15)

        if not self.no_text:
            msg = self.font.render(self.text, False, self.font_color)
            msg_rect = msg.get_rect()
            msg_rect.center = self.rect.center
            self.display_surf.blit(msg, msg_rect)

    def check_pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        left_mouse_button_clicked = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_pos) and left_mouse_button_clicked:
            self.pressed = True


class TriangleButton(Button):
    def __init__(self, display_surface: pygame.Surface, color, pos, direction):
        super().__init__(display_surface, color, pos)
        self.direction = direction
        self.size = 30
        self.points = self.calculate_pos()

    def display(self):
        self.rect = pygame.draw.polygon(self.display_surf, self.color, self.points)

    def calculate_pos(self):
        """Calculate the points to draw the requested triangle."""
        x, y = self.pos
        half = self.size // 2
        if self.direction == "right":
            # Points:    Left             Top-right           Bottom-right
            return [(x - half, y), (x + half, y - half), (x + half, y + half)]

        if self.direction == "left":
            # Points:   Right            Top-left             Bottom-left
            return [(x + half, y), (x - half, y - half), (x - half, y + half)]


class SettingChoice:
    def __init__(self, height, msg, button_color, box_color, font_color, color_to_change):
        self.display_surf = pygame.display.get_surface()
        self.height = height
        self.color = color_to_change

        self.right_button = TriangleButton(self.display_surf, button_color,
                                           (SCREEN_WIDTH - 200, self.height), "right")

        self.left_button = TriangleButton(self.display_surf, button_color,
                                          (SCREEN_WIDTH - 100, self.height), "left")

        self.font = pygame.font.SysFont(None, 32)
        self.font_color = font_color
        self.name = msg
        self.box_color = box_color

    def update(self):
        self.right_button.display()
        self.left_button.display()

        msg = self.font.render(self.name, False, self.font_color)
        self.display_surf.blit(msg, (SCREEN_HEIGHT - 500, self.height))

        pygame.draw.rect(self.display_surf, self.box_color,
                         (SCREEN_WIDTH - 170, self.height - 20, 40, 40), 5)

        # Manual manipulation by adding or subtracting 5
        pygame.draw.rect(self.display_surf, self.color,
                         (SCREEN_WIDTH - 165, self.height - 15, 30, 30))

    def is_pressed(self):
        self.right_button.check_pressed()
        self.left_button.check_pressed()

        if self.left_button.pressed:
            return "left"

        if self.right_button.pressed:
            return "right"
