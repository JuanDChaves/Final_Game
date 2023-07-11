import pygame
import sys
import json
from settings import *
from screens import *
from levels import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        with open("Final_Game/files/buttons.json") as file:
            self.buttons_dict = json.load(file)
        self.new_game()

    def new_game(self):
        self.game_state = "main"
        self.current_screen = Current_screen(self)
        self.current_level = Level(self)
        self.hero = Hero(self, HERO_X, HERO_Y)
        self.bullet_group = pygame.sprite.Group()

    def state_handler(self):
        match self.game_state:
            case "main":
                self.id = "main"
                self.current_screen.draw(self.id)
            case "play":
                self.playing = True
                self.id = "play"
                self.current_screen.draw(self.id)

                scroll = self.hero.scroll

                self.current_level.update(scroll)
                scrolled = self.current_level.scrolled
                self.hero.draw(scrolled)

                self.current_level.draw()

                self.bullet_group.update()
                self.bullet_group.draw(self.screen)
                # self.enemies
            case "levels":
                self.id = "levels"
                self.current_screen.draw(self.id)
            case "settings":
                self.id = "settings"
                self.current_screen.draw(self.id)
            case "best":
                self.id = "best"
                self.current_screen.draw(self.id)
            case "about":
                self.id = "levels"
                self.current_screen.draw(self.id)
            case "quit":
                pygame.quit()
                sys.exit()

    def update(self):
        self.delta_ms = self.clock.tick(FPS)
        self.state_handler()
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()


if __name__ == "__main__":
    game = Game()
    game.run()
