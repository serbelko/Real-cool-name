import pygame
from sprites import sprite_sheets
from settings import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sprite_sheet_image = pygame.image.load('sprites/walk1.png').convert_alpha()
sprite_sheet = sprite_sheets.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)

animation_list = []
animation_steps = [8, 8, 8, 8, 8, 8]
action = 4
steps_counter = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 150
frame = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(steps_counter, 48, 64, 3, BLACK))
        steps_counter += 1
    animation_list.append(temp_img_list)

run = True
while run:

    screen.fill(BG)

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    screen.blit(animation_list[action][frame], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                action = 0
                frame = 0
            if event.key == pygame.K_w:
                action = 3
                frame = 0
            if event.key == pygame.K_a:
                action = 1
                frame = 0
            if event.key == pygame.K_d:
                action = 5
                frame = 0

    pygame.display.update()
pygame.quit()
