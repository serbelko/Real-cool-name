import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import sys

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("map.png").convert()

# Параметры для прокрутки
camera_x = 0
camera_y = 0
camera_speed = 5

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получаем нажатые клавиши
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= camera_speed
    if keys[pygame.K_RIGHT]:
        camera_x += camera_speed
    if keys[pygame.K_UP]:
        camera_y -= camera_speed
    if keys[pygame.K_DOWN]:
        camera_y += camera_speed

    # Отрисовываем изображение с учетом смещения камеры
    screen.fill((0, 0, 0))  # Очистка экрана
    screen.blit(background_image, (camera_x, camera_y))

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем FPS
    pygame.time.Clock().tick(60)