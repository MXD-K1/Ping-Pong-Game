import time

import pygame

from settings import *
from colors import get_color, set_color, change_color
from timer import Timer


class StartScreen:
    def __init__(self, colors):
        self.colors = colors
        self.display_surf = pygame.display.get_surface()

        self.font = pygame.font.SysFont(None, 48)
        self.play_button = Button(self.display_surf, get_color(self.colors, 'button'),
                                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),
                                  "Play", 42,
                                  get_color(self.colors, 'button text'))

        self.settings_button = Button(self.display_surf, get_color(self.colors, 'button'),
                                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                      "Settings", 32, get_color(self.colors, 'button text'))

        self.welcome_label = Label(self.display_surf, "Welcome to Ping Pong", get_color(self.colors, "text"),
                                   (SCREEN_WIDTH // 2, 50))

        self.one_player_button = Button(self.display_surf, get_color(self.colors, 'button'),
                                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),
                                        "1 Player", 32, get_color(self.colors, 'button text'))

        self.two_players_button = Button(self.display_surf, get_color(self.colors, 'button'),
                                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30),
                                         "2 Players", 32, get_color(self.colors, 'button text'))

        self.wait_timer = Timer(1000)
        self.wait_timer.activate()

    def re_init(self):
        self.play_button.color = get_color(self.colors, 'button')
        self.play_button.font_color = get_color(self.colors, 'button text')
        self.settings_button.color = get_color(self.colors, 'button')
        self.settings_button.font_color = get_color(self.colors, 'button text')
        self.one_player_button.color = get_color(self.colors, 'button')
        self.one_player_button.font_color = get_color(self.colors, 'button text')
        self.two_players_button.color = get_color(self.colors, 'button')
        self.two_players_button.font_color = get_color(self.colors, 'button text')
        # No need to change the color of the labels here because they are changed in show_settings.

    def update(self):
        if self.settings_button.pressed:
            self.show_settings()
        elif self.play_button.pressed:
            self.display_playing_menu()
            self.wait_timer.update()
            print(self.wait_timer.active)
            if not self.wait_timer.active:
                self.check_playing_sub_buttons_pressed()
        else:
            self.play_button.draw()
            self.settings_button.draw()
            self.welcome_label.draw()
            self.settings_button.check_pressed()

    def show_settings(self):
        label = Label(self.display_surf, "Choose the mode color you want", get_color(self.colors, 'text'),
                      (SCREEN_WIDTH // 2, 50))
        label.draw()

        return_button = Button(self.display_surf, get_color(self.colors, 'button'),
                               (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100),
                               "Return", 42, get_color(self.colors, 'button text'))

        color_choices = ['Screen', 'Paddle 1', 'Paddle 2', 'Ball']
        settings = []
        for index, choice in enumerate(color_choices, 1):
            setting_colors = {'button': get_color(self.colors, 'button'),
                              'box': get_color(self.colors, 'box'),
                              'text': get_color(self.colors, 'text'),
                              choice.lower(): get_color(self.colors, choice.lower())
                              }

            settings.append(SettingChoice((SCREEN_HEIGHT - 450 + 50 * index), choice, setting_colors['button'],
                                          setting_colors['box'], setting_colors['text'],
                                          setting_colors[choice.lower()]))

        return_button.draw()

        for setting in settings:
            setting.update()
            if setting.is_pressed() == "right":
                change_color(self.colors, setting.name.lower(), -1)

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
                change_color(self.colors, setting.name.lower(), 1)

                if self.colors[setting.name.lower()]['pos'] < 0:
                    set_color(self.colors, setting.name.lower(), len(self.colors[setting.name.lower()]['colors']) - 1)
                elif self.colors[setting.name.lower()]['pos'] > len(self.colors[setting.name.lower()]['colors']) - 1:
                    set_color(self.colors, setting.name.lower(), 0)

                if setting.name.lower() == 'screen':
                    self.colors['text']['pos'] = self.colors['screen']['pos']
                    self.colors['button']['pos'] = self.colors['screen']['pos']
                    self.colors['button text']['pos'] = self.colors['screen']['pos']

                time.sleep(0.2)  # to add it once only

        return_button.check_pressed()
        if return_button.pressed:
            self.settings_button.pressed = False

        self.re_init()

    def display_playing_menu(self):
        return_button = Button(self.display_surf, get_color(self.colors, 'button'),
                               (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40),
                               "Return", 42, get_color(self.colors, 'button text'))

        self.one_player_button.draw()
        self.two_players_button.draw()
        return_button.draw()

        return_button.check_pressed()
        if return_button.pressed:
            self.play_button.pressed = False

    def start_game(self):
        self.play_button.check_pressed()
        if self.play_button.pressed:
            if self.one_player_button.pressed:
                return True, 1
            elif self.two_players_button.pressed:
                return True, 2
        return False, 0

    def check_playing_sub_buttons_pressed(self):
        self.one_player_button.check_pressed()
        self.two_players_button.check_pressed()


class Label:
    def __init__(self, display_surface: pygame.Surface, text, color, pos: tuple[int, int], size=48):
        self.display_surf = display_surface
        self.text = text
        self.color = color
        self.pos = pos

        self.font = pygame.font.SysFont(None, size)

    def draw(self):
        text = self.font.render(self.text, True, self.color)
        self.display_surf.blit(text, (self.pos[0] - text.get_width() // 2, self.pos[1]))


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
        else:
            self.text = None

        self.height, self.width = 60, 120
        self.rect = pygame.rect.Rect(pos[0], pos[1], self.width, self.height)
        self.rect.x -= self.rect.width // 2
        self.rect.y -= self.rect.height // 2

        self.pressed = False

    def draw(self):
        pygame.draw.rect(self.display_surf, self.color, self.rect, border_radius=15)

        if self.text:
            msg = self.font.render(self.text, True, self.font_color)
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

    def draw(self):
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
        self.box_color = box_color
        self.name = msg

        self.right_button = TriangleButton(self.display_surf, button_color,
                                           (SCREEN_WIDTH - 200, self.height), "right")

        self.left_button = TriangleButton(self.display_surf, button_color,
                                          (SCREEN_WIDTH - 100, self.height), "left")

        self.label = Label(self.display_surf, self.name, font_color,
                           (SCREEN_HEIGHT - 450, self.height), 32)
        self.font = pygame.font.SysFont(None, 32)

    def update(self):
        self.right_button.draw()
        self.left_button.draw()

        self.label.draw()

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
