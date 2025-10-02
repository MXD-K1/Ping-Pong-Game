from pygame.time import wait

from colors import get_color, change_color
from ui_components import *  # pygame and settings are imported from here
from timer import Timer


class StartScreen:
    def __init__(self, colors):
        self.colors = colors
        self.display_surf = pygame.display.get_surface()

        self.font = pygame.font.SysFont(None, 48)
        self.play_button = Button(get_color('button'),
                                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),
                                  "Play", "big",
                                  get_color('button text'))

        self.settings_button = Button(get_color('button'),
                                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                      "Settings", "small", get_color('button text'))

        self.welcome_label = Label("Welcome to Ping Pong", get_color("text"),
                                   (SCREEN_WIDTH // 2, 50), fonts['heading'])

        self.one_player_button = Button(get_color('button'),
                                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),
                                        "1 Player", "small", get_color('button text'))

        self.two_players_button = Button(get_color('button'),
                                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30),
                                         "2 Players", "small", get_color('button text'))

        self.wait_timer = Timer(2000)
        self.wait_timer.activate()

    def re_init(self):
        self.play_button.color = get_color('button')
        self.play_button.font_color = get_color('button text')
        self.settings_button.color = get_color('button')
        self.settings_button.font_color = get_color('button text')
        self.one_player_button.color = get_color('button')
        self.one_player_button.font_color = get_color('button text')
        self.two_players_button.color = get_color('button')
        self.two_players_button.font_color = get_color('button text')
        # No need to change the color of the labels here because they are changed in show_settings.

    def update(self):
        if self.settings_button.pressed:
            self.show_settings()
        elif self.play_button.pressed:
            self.display_playing_menu()
            self.wait_timer.update()
            if not self.wait_timer.active:
                self.check_playing_sub_buttons_pressed()
        else:
            self.draw_main_screen()
            self.settings_button.check_pressed()

    def draw_main_screen(self):
        self.play_button.draw()
        self.settings_button.draw()
        self.welcome_label.draw()

    def show_settings(self):
        label = Label("Settings", get_color('text'),
                      (SCREEN_WIDTH // 2, 50), fonts['heading'])
        label.draw()

        return_button = Button(get_color('button'),
                               (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100),
                               "Return", "big", get_color('button text'))

        color_choices = ['Paddle 1', 'Paddle 2', 'Ball']
        settings = []
        for index, choice in enumerate(color_choices, 1):
            setting_colors = {'button': get_color('button'),
                              'box': get_color('box'),
                              'text': get_color('text'),
                              choice.lower(): get_color(choice.lower())
                              }

            settings.append(SettingChoice((SCREEN_HEIGHT - 450 + 50 * index), choice, setting_colors['button'],
                                          setting_colors['box'], setting_colors['text'],
                                          setting_colors[choice.lower()]))

        return_button.draw()

        for setting in settings:
            setting.draw()
            if setting.is_pressed() == "right":
                change_color(setting.name.lower(), -1)
                wait(200)  # to add it once

            elif setting.is_pressed() == "left":
                change_color(setting.name.lower())
                wait(200)  # to add it once only

        return_button.check_pressed()
        if return_button.pressed:
            self.settings_button.reset()

        self.re_init()

    def display_playing_menu(self):
        return_button = Button(get_color('button'),
                               (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40),
                               "Return", "big", get_color('button text'))

        self.one_player_button.draw()
        self.two_players_button.draw()
        return_button.draw()

        return_button.check_pressed()
        if return_button.pressed:
            self.play_button.reset()

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
