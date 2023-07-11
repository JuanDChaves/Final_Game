import pygame
from settings import *
from button import *
from hero import *


class Current_screen:
    def __init__(self, game) -> None:
        self.game = game
        self.clicked = False

    def get_image_names(self):
        pass

    def draw(self, id):
        self.draw_screen()
        if id != "play":
            for key, value in self.game.buttons_dict[id].items():
                self.draw_button(key, value[0], value[1])

    def draw_screen(self):
        self.game.screen.fill((10, 10, 0))

    def draw_button(self, key, image_name, x_y):
        self.button = Button(key, x_y[0], x_y[1], image_name)
        self.game.screen.blit(self.button.image, x_y)

        self.detect_collisions()

    def detect_collisions(self):
        self.pos = pygame.mouse.get_pos()

        if self.button.rect.collidepoint(self.pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if self.button.key == "back":
                    self.game.game_state = "main"
                else:
                    self.game.game_state = self.button.key
                pygame.display.set_caption(self.button.key.capitalize())

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
