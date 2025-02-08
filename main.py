# комментарий для коммита

import random
import sys
from settings import *
import pygame
from sprites import *  # комментарий для коммита

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


def instruction():
    instruction_start_time = pygame.time.get_ticks()
    show_continue_text = False

    running = True



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
                    screen.blit(instructions, (0, 0))
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
        screen.fill(BLACK)
        shop_text = font.render("SHOP", True, WHITE)
        boots_button = font.render("SPEEDY BOOTS", True, WHITE)
        stone_button = font.render("HEALING STONE", True, WHITE)
        shield_button = font.render("MAGIC SHIELD", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        screen.blit(shop_text, (SCREEN_WIDTH // 2 - shop_text.get_width() // 2, 100))
        screen.blit(boots_button, (15, 250))
        screen.blit(stone_button, (SCREEN_WIDTH // 2 - stone_button.get_width() // 2, 250))
        screen.blit(shield_button, (SCREEN_WIDTH - 200, 250))
        screen.blit(exit_button, (SCREEN_WIDTH // 2 - exit_button.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if exit_button.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
                    return
                if boots_button.get_rect(center=(15, 250)).collidepoint(mouse_x, mouse_y):
                    player.speed += 5
                    return
                if stone_button.get_rect(center=(SCREEN_WIDTH // 2, 250)).collidepoint(mouse_x, mouse_y):
                    player.health += 20
                    return
                if shield_button.get_rect(center=(SCREEN_WIDTH - 200, 250)).collidepoint(mouse_x, mouse_y):
                    player.health += 2
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


class Map:
    def __init__(self, fight_arena, SCREEN_WIDTH, SCREEN_HEIGHT):
        # Загрузка изображения карты
        self.image = pygame.image.load('fight_arena.png').convert()
        self.rect = self.image.get_rect()

        # Создание хитбоксов (10 пикселей от краев окна)
        self.hitboxes = [
            pygame.Rect(0, 0, SCREEN_WIDTH, 10),  # Верхний хитбокс
            pygame.Rect(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10),  # Нижний хитбокс
            pygame.Rect(0, 0, 10, SCREEN_HEIGHT),  # Левый хитбокс
            pygame.Rect(SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT)  # Правый хитбокс
        ]

    def draw(self, screen):
        # Отрисовка карты на экране.
        screen.blit(self.image, self.rect)

    def draw_hitboxes(self, screen):
        # """Отрисовка хитбоксов (для отладки)."""
        for hitbox in self.hitboxes:
            pygame.draw.rect(screen, RED, hitbox, 2)

    def check_collision(self, sprite):
        # """Проверка столкновения спрайта с хитбоксами."""
        for hitbox in self.hitboxes:
            if sprite.rect.colliderect(hitbox):
                return True
        return False


while running:
    keys = pygame.key.get_pressed()
    screen.fill(BLACK)

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
