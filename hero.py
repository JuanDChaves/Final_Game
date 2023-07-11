import pygame
from settings import *
from bullet import *


class Hero:
    def __init__(self, game, x, y) -> None:
        self.game = game
        self.hero_x = x
        self.hero_y = y
        self.hero_center_x = 0
        self.hero_center_y = 0
        self.jumping = False
        self.shooting = False
        self.direcion_r = False
        self.direcion_l = False
        self.scroll = 0
        self.shoot_direction = True  # True - Right / False - Left
        self.vertical_speed = 0  # se puede poner de una vez en -10?
        self.update_time = pygame.time.get_ticks()
        self.sprite_sheet_image = pygame.image.load(
            "Final_Game/Sprites/Jump.png"
        ).convert_alpha()
        self.sprite_sheet_image_len = self.sprite_sheet_image.get_width()
        self.frame = 0
        self.number_of_frames = 0
        for _ in range(int(self.sprite_sheet_image_len / 200) - 1):
            self.number_of_frames += 1
        print("num fr: ", self.number_of_frames)
        self.black = (0, 0, 0)
        self.hero_rect = pygame.Rect(self.hero_x, self.hero_y, 50, 50)

    def shoot(self):
        self.hero_center_x = self.hero_rect.centerx + self.delta_x
        self.hero_center_y = self.hero_rect.centery + self.delta_y

        if self.shoot_direction:
            self.bullet = Bullet(
                self.game,
                self.hero_center_x + 60,
                self.hero_center_y,
                self.shoot_direction,
            )
        else:
            self.bullet = Bullet(
                self.game,
                self.hero_center_x - 60,
                self.hero_center_y,
                self.shoot_direction,
            )
        self.game.bullet_group.add(self.bullet)

    def actions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direcion_r = True
            self.shoot_direction = True
        if not keys[pygame.K_d]:
            self.direcion_r = False

        if keys[pygame.K_a]:
            self.direcion_l = True
            self.shoot_direction = False
        if not keys[pygame.K_a]:
            self.direcion_l = False

        if keys[pygame.K_j]:
            self.shooting = True
        if not keys[pygame.K_j]:
            self.shooting = False

        if keys[pygame.K_w] and self.hero_rect.bottom >= 449:
            self.jumping = True
        if not keys[pygame.K_w]:
            self.jumping = False

    def movement(self, scrolled):
        # hacer que no se mueva mas cuando muere
        self.delta_x = 0
        self.delta_y = 0
        self.scroll = 0
        self.scrolled = scrolled

        if self.direcion_r == True:
            if scrolled == 1600 and self.hero_rect.right <= 800:
                self.delta_x += HERO_SPEED
            else:
                if self.hero_rect.right > WINDOW_WIDTH - SCROLL_LIMIT:
                    self.delta_x = 0
                    self.scroll = -HERO_SPEED
                else:
                    self.scroll = 0
                    self.delta_x += HERO_SPEED

        if self.direcion_l == True:
            if scrolled <= 0 and self.hero_rect.left > 0:
                self.delta_x -= HERO_SPEED
            else:
                if self.hero_rect.left < SCROLL_LIMIT:
                    self.delta_x = 0
                    self.scroll = HERO_SPEED
                else:
                    self.delta_x -= HERO_SPEED

        if self.jumping == True:
            if self.hero_rect.top < 0:
                self.vertical_speed = 0
            else:
                self.vertical_speed = -15

        self.vertical_speed += GRAVITY
        self.delta_y += self.vertical_speed

        if self.hero_rect.bottom + self.delta_y > 450:  # colision temporal
            self.delta_y = 450 - self.hero_rect.bottom

        self.hero_x += self.delta_x
        self.hero_y += self.delta_y

    def load_sprite(self, sheet, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image

    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
            if self.frame > self.number_of_frames:
                self.frame = 0

    def draw(self, scrolled):
        self.movement(scrolled)
        if self.shooting:
            self.shoot()
        self.actions()
        self.update_animation()
        self.image = self.load_sprite(
            self.sprite_sheet_image, self.frame, 200, 200, 1.5, (0, 0, 0)
        )
        self.hero_rect.x = self.hero_x
        self.hero_rect.y = self.hero_y

        pygame.draw.rect(self.game.screen, (50, 45, 250), self.hero_rect, 4)
        self.game.screen.blit(self.image, (self.hero_rect.x, self.hero_rect.y))


# for event in pygame.event.get():
#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_w:
#             self.jumping = True
#     if event.type == pygame.KEYUP:
#         if event.key == pygame.K_w:
#             self.jumping = False
