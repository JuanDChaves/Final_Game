import pygame


class Button:
    def __init__(self, key, x, y, image) -> None:
        self.key = key
        self.image = pygame.image.load(f"Final_Game/images/{image}.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
