import pygame
from settings import *
from hero import *
from maps import *


class Level:
    def __init__(self, game) -> None:
        self.game = game
        self.level_width = LEVEL_WIDTH
        self.level_height = LEVEL_HEIGHT
        self.tile_init_x = 0
        self.tile_init_y = 0
        self.scrolled = 0
        self.maps = Maps()
        self.tile = pygame.Rect(
            self.tile_init_x, self.tile_init_y, TILE_WIDTH, TILE_HEIGHT
        )

    def update(self, scroll):
        self.tile_init_x += scroll
        self.scrolled = -self.tile_init_x
        if self.scrolled <= 0 or self.scrolled >= 1600:
            self.tile_init_x -= scroll

    def draw(self):
        self.map_1 = self.maps.map_1()
        for row in range(TILE_ROWS):
            for col in range(TILE_COLUMNS):
                self.tile.x = col * TILE_WIDTH + self.tile_init_x
                self.tile.y = row * TILE_HEIGHT
                if self.map_1[row][col] == 1:
                    pygame.draw.rect(self.game.screen, (200, 200, 255), self.tile)
                # else:
                #     pygame.draw.rect(self.game.screen, (50, 50, 50), self.tile, 1)
