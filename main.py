# комментарий для коммита

import random
import sys
from settings import *
import pygame
from sprites import *

pygame.init()
from settings import *

# Инициализация окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Real Cool game")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
last_shot_time = 0

player = Player()
player_group = pygame.sprite.Group(player)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
current_wave_enemies = pygame.sprite.Group()
enemies_to_spawn = 10  # Количество врагов в волне (можно изменять для разных волн)
spawned_enemies = 0  # Счетчик заспавненных врагов
menu_bg = pygame.image.load('assetspngs/main_menu.png').convert_alpha()
pause_bg = pygame.image.load('assetspngs/pause_menu.png').convert_alpha()
instructions = pygame.image.load('assetspngs/instructions.png').convert_alpha()
enter = pygame.image.load('assetspngs/ENTER.png').convert_alpha()
shop = pygame.image.load('assetspngs/shop_menu.png').convert_alpha()
map1 = pygame.image.load('assetspngs/maps/map1.png').convert_alpha()
def settings_menu():
    while True:
        screen.fill(BLACK)
        settings_text = font.render("Settings Menu", True, WHITE)
        back_button_text = font.render("Back", True, WHITE)

        screen.blit(settings_text, (SCREEN_WIDTH // 2 - settings_text.get_width() // 2, 200))
        screen.blit(back_button_text, (SCREEN_WIDTH // 2 - back_button_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if back_button_text.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
                    return



def show_instructions():
    instruction_start_time = pygame.time.get_ticks()  # Get current time
    show_continue_text = False  # Track when to show the "Press Enter" text

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(instructions, (0, 0))  # Show instructions image

        # Check if 10 seconds have passed
        if pygame.time.get_ticks() - instruction_start_time > 2000:
            show_continue_text = True  # Show "Press Enter to Continue"

        if show_continue_text:
            text_surface = font.render("Press ENTER to continue", True, (255, 255, 255))
            screen.blit(text_surface, (250, 560))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and show_continue_text:
                if event.key == pygame.K_RETURN:
                    return


def main_menu():
    while True:
        screen.blit(menu_bg, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 349 <= mouse_x <= 466 and 250 <= mouse_y <= 303:
                    show_instructions()
                    return
                if 349 <= mouse_x <= 466 and 313 <= mouse_y <= 370:
                    settings_menu()
                if 349 <= mouse_x <= 466 and 370 <= mouse_y <= 430:
                    pygame.quit()
                    sys.exit()


def game_over():
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        reload_button = font.render("Reload Game", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(reload_button, (SCREEN_WIDTH // 2 - reload_button.get_width() // 2, 300))
        screen.blit(exit_button, (SCREEN_WIDTH // 2 - exit_button.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if reload_button.get_rect(center=(SCREEN_WIDTH // 2, 300)).collidepoint(mouse_x, mouse_y):
                    return True
                if exit_button.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
    return False


def pause_menu():
    while True:
        screen.blit(pause_bg, (0, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 341 <= mouse_x <= 458 and 250 <= mouse_y <= 303:
                    return
                if 341 <= mouse_x <= 458 and 315 <= mouse_y <= 368:
                    pygame.quit()
                    sys.exit()


def skill_upgrade():
    while True:
        screen.blit(shop, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 214 <= mouse_x <= 296 and 146 <= mouse_y <= 228:
                    player.strength += 5
                    player.currency -= 100
                    return
                if 214 <= mouse_x <= 296 and 272 <= mouse_y <= 354:
                    player.strength += 5
                    player.currency -= 200
                    return
                if 214 <= mouse_x <= 296 and 399 <= mouse_y <= 481:
                    player.strength += 5
                    player.currency -= 300
                    return
                #first collum
                if 370 <= mouse_x <= 425 and 146 <= mouse_y <= 228:
                    player.health += 10
                    player.currency -= 100
                    return
                if 370 <= mouse_x <= 425 and 272 <= mouse_y <= 354:
                    player.health += 20
                    player.currency -= 200
                    return
                if 370 <= mouse_x <= 425 and 399 <= mouse_y <= 481:
                    player.health += 50
                    player.currency -= 300
                    return
                #second collum
                if 526 <= mouse_x <= 608 and 146 <= mouse_y <= 228:
                    player.speed += 3
                    player.currency -= 100
                    return
                if 526 <= mouse_x <= 608 and 272 <= mouse_y <= 354:
                    player.speed += 3
                    player.currency -= 200
                    return
                if 526 <= mouse_x <= 608 and 399 <= mouse_y <= 481:
                    player.speed += 3
                    player.currency -= 300
                    return




def reset_game():
    global player, player_group, bullets, enemies, enemy_bullets, last_shot_time
    player = Player()
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    last_shot_time = 0


def next_wave():
    global wave_active, enemies_to_spawn, spawned_enemies, current_wave_enemies
    wave_active = True
    enemies_to_spawn += 5  # Увеличиваем сложность волн (можно менять)
    spawned_enemies = 0  # Обнуляем счетчик заспавненных врагов
    current_wave_enemies.empty()  # Очищаем группу врагов


def spawn_enemy():
    if len(enemies) < enemies_to_spawn:
        if random.random() < 0.5:
            enemy = MeleeEnemy()
        else:
            enemy = RangedEnemy()
        enemies.add(enemy)


# --------------------------------------------------------------------- #
#                         ЗАПУСК ИГРЫ                                   #
# --------------------------------------------------------------------- #

main_menu()

spawn_enemy_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_enemy_event, 2000)  # Спавним врагов каждые 2 секунды

running = True

while running:
    keys = pygame.key.get_pressed()
    screen.blit(map1, (0, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Переключение оружия у игрока
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.switch_weapon('gun')
            elif event.key == pygame.K_2:
                player.switch_weapon('melee')

            # Пауза
            if event.key == pygame.K_p:
                pause_menu()

            # Пробел
            if event.key == pygame.K_SPACE:
                if player.weapon == 'gun':
                    current_time = pygame.time.get_ticks()
                    if current_time - last_shot_time > RELOAD_DELAY:
                        last_shot_time = current_time
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y)
                        bullets.add(bullet)
                else:
                    player.start_melee_attack()

        # Клик ЛКМ
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player.weapon == 'gun':
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time > RELOAD_DELAY:
                    last_shot_time = current_time
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y)
                    bullets.add(bullet)
            else:
                player.start_melee_attack()

        # Клик V - волна
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v and not wave_active:
                next_wave()

        # Спавн врагов
        if event.type == spawn_enemy_event and wave_active and spawned_enemies < enemies_to_spawn:

            current_time = pygame.time.get_ticks()
            if current_time - spawn_timer > spawn_interval:
                spawn_timer = current_time
                if random.random() < 0.5:
                    enemy = MeleeEnemy()
                else:
                    enemy = RangedEnemy()

                enemies.add(enemy)
                current_wave_enemies.add(enemy)
                spawned_enemies += 1

        if wave_active and spawned_enemies == enemies_to_spawn and len(current_wave_enemies) == 0:
            print("Волна закончена")
            wave_active = False
            skill_upgrade()

    # Обновления
    player.update(keys)
    bullets.update()
    enemy_bullets.update()

    for enemy in enemies:
        if isinstance(enemy, MeleeEnemy):
            enemy.update(player)
        elif isinstance(enemy, RangedEnemy):
            enemy.update(player)

    # Ближняя атака игрока
    if player.weapon == 'melee':
        player.update_melee_attack(enemies)

    # Пули игрока против врагов
    for enemy in current_wave_enemies:
        while pygame.sprite.spritecollide(enemy, bullets, True):
            enemy.hp -= player.strength
            print(enemy.hp)
            if enemy.hp <= 0:
                enemy.kill()
                enemies_killed += 1
                current_wave_enemies.remove(enemy)
                player.currency += 10

    # Вражеские пули против игрока
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for _ in hits:
        player.health -= 10
        print("Player hit by enemy bullet! HP:", player.health)

    # Проверяем, не умер ли игрок
    if player.health <= 0:
        if game_over():
            reset_game()
        else:
            running = False
            break

    # Отрисовка
    player_group.draw(screen)
    bullets.draw(screen)
    enemy_bullets.draw(screen)
    enemies.draw(screen)

    # Визуализация ближней атаки (хитбокс)
    if player.is_attacking and player.weapon == 'melee':
        pygame.draw.rect(screen, YELLOW, player.attack_rect, width=2)

    # Отображаем здоровье игрока
    health_text = font.render(f"HP: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 10))

    # Отображаем кошелек игрока
    currency_text = font.render(f'GOLD: {player.currency}', True, WHITE)
    screen.blit(currency_text, (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
