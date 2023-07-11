import pygame

pygame.init()


screen = pygame.display.set_mode((500, 500))

sprite_sheet_image = pygame.image.load("Final_Game/Sprites/Idle.png").convert_alpha()


def get_image(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)

    return image


frame_0 = get_image(sprite_sheet_image, 0, 200, 200, 1.5, (0, 0, 0))
frame_1 = get_image(sprite_sheet_image, 1, 200, 200, 1.5, (0, 0, 0))


run = True
while run:
    screen.fill((50, 50, 50))

    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (200, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
