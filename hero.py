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
        self.manage_sprite_sheet()
        self.hero_rect = self.get_hero_rect()
        # self.hero_rect = pygame.Rect(self.hero_x, self.hero_y, 50, 50)

    def get_hero_rect(self):
        self.image = self.load_sprite(
            self.sprite_sheet_image, self.frame, 64, 80, 1, (0, 0, 0)
        )
        new_rect = self.image.get_rect()
        return new_rect

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

    def get_obstacles(self, obstacles):
        self.obstacles_list = obstacles
        self.temp_rect_list = []
        for obstacle in self.obstacles_list:
            temp_rect = pygame.Rect(obstacle[0], obstacle[1], 50, 50)
            self.temp_rect_list.append(temp_rect)

    def movement(self, scrolled, obstacles):
        # hacer que no se mueva mas cuando muere
        self.delta_x = 0
        self.delta_y = 0
        self.scroll = 0
        self.scrolled = scrolled
        self.get_obstacles(obstacles)
        # self.obstacles_list = obstacles

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

        # if self.hero_rect.collidelist(self.temp_rect_list) >= 0:
        #     print("collision")
        #     self.delta_x = 1
        #     self.delta_y = 1

        for rect in self.temp_rect_list:
            # if rect.colliderect(
            #     self.hero_x + self.delta_x, self.hero_y, TILE_WIDTH, TILE_HEIGHT
            # ):
            #         self.delta_x = 0
            #         print("collision x")
            if rect.colliderect(
                self.hero_x, self.hero_y + self.delta_y, TILE_WIDTH, TILE_HEIGHT
            ):
                self.delta_y = 0
                print("collision y", "hero x: ", self.hero_x, "hero y: ", self.hero_y)

        self.hero_x += self.delta_x
        self.hero_y += self.delta_y

    def manage_sprite_sheet(self):
        self.sprite_sheet_image = pygame.image.load(
            "Final_Game/Sprites/ghost-idle.png"
        ).convert_alpha()
        self.sprite_sheet_image_len = self.sprite_sheet_image.get_width()
        self.frame = 0
        self.number_of_frames = 0
        for _ in range(int(self.sprite_sheet_image_len / 64) - 1):
            self.number_of_frames += 1
        self.black = (0, 0, 0)

    def load_sprite(self, sheet, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image = pygame.transform.flip(image, True, False)
        image.set_colorkey(color)

        return image

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

    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
            if self.frame > self.number_of_frames:
                self.frame = 0

    def draw(self, scrolled, obstacles):
        self.movement(scrolled, obstacles)
        if self.shooting:
            self.shoot()
        self.actions()
        self.update_animation()
        self.hero_rect.x = self.hero_x
        self.hero_rect.y = self.hero_y

        pygame.draw.rect(self.game.screen, (50, 45, 250), self.hero_rect, 4)
        for rect in self.temp_rect_list:
            pygame.draw.rect(
                self.game.screen,
                (0, 250, 0),
                rect,
            )
        self.game.screen.blit(self.image, (self.hero_x, self.hero_y))


# for event in pygame.event.get():
#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_w:
#             self.jumping = True
#     if event.type == pygame.KEYUP:
#         if event.key == pygame.K_w:
#             self.jumping = False
