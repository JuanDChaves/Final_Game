from typing import Any
import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction) -> None:
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.direction = direction
        self.bullet_speed = 10
        self.image = pygame.image.load("Final_Game/images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # self.direction = direction

    def update(self) -> None:
        if self.direction:
            self.rect.x += self.bullet_speed
        else:
            self.rect.x -= self.bullet_speed

        if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH:
            self.kill()
