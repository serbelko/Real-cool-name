import random
import sys

import pygame

pygame.init()

# --- Константы ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

PLAYER_SPEED = 5
BULLET_SPEED = 10
RELOAD_DELAY = 200

# Параметры ближней атаки у игрока
ATTACK_COOLDOWN = 500
ATTACK_DURATION = 200
HITBOX_WIDTH = 50
HITBOX_HEIGHT = 30


wave_active = False
enemies_to_spawn = 0
enemies_killed = 0
spawn_timer = 0
spawn_interval = 2000

PLAYER_MAX_HEALTH = 1000000000



# Инициализация окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Real Cool game")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
last_shot_time = 0


# --------------------------------------------------------------------- #
#                           КЛАССЫ                                      #
# --------------------------------------------------------------------- #

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Текущее оружие (gun / melee)
        self.weapon = 'gun'

        # Для ближней атаки
        self.is_attacking = False
        self.last_attack_time = 0
        self.attack_rect = pygame.Rect(0, 0, HITBOX_WIDTH, HITBOX_HEIGHT)

        # Направление игрока (up, down, left, right)
        self.direction = 'down'

        # Здоровье
        self.health = PLAYER_MAX_HEALTH

    def switch_weapon(self, new_weapon):
        self.weapon = new_weapon
        self.is_attacking = False

    def update_direction(self, dx, dy):
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy < 0:
            self.direction = 'up'
        elif dy > 0:
            self.direction = 'down'

    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_w] and self.rect.top > 0:
            dy -= PLAYER_SPEED
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            dy += PLAYER_SPEED
        if keys[pygame.K_a] and self.rect.left > 0:
            dx -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            dx += PLAYER_SPEED

        self.rect.x += dx
        self.rect.y += dy

        if dx != 0 or dy != 0:
            self.update_direction(dx, dy)

    def start_melee_attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= ATTACK_COOLDOWN:
            self.is_attacking = True
            self.last_attack_time = current_time

    def update_melee_attack(self, enemies_group):
        if self.is_attacking:
            current_time = pygame.time.get_ticks()
            time_since_attack = current_time - self.last_attack_time

            if time_since_attack <= ATTACK_DURATION:
                if self.direction == 'up':
                    self.attack_rect.width, self.attack_rect.height = HITBOX_WIDTH, HITBOX_HEIGHT
                    self.attack_rect.midbottom = self.rect.midtop
                elif self.direction == 'down':
                    self.attack_rect.width, self.attack_rect.height = HITBOX_WIDTH, HITBOX_HEIGHT
                    self.attack_rect.midtop = self.rect.midbottom
                elif self.direction == 'left':
                    self.attack_rect.width, self.attack_rect.height = HITBOX_HEIGHT, HITBOX_WIDTH
                    self.attack_rect.midright = self.rect.midleft
                elif self.direction == 'right':
                    self.attack_rect.width, self.attack_rect.height = HITBOX_HEIGHT, HITBOX_WIDTH
                    self.attack_rect.midleft = self.rect.midright

                for enemy in enemies_group:
                    if self.attack_rect.colliderect(enemy.rect):
                        enemy.kill()
            else:
                self.is_attacking = False


class Bullet(pygame.sprite.Sprite):
    """Пуля игрока."""

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        direction = pygame.math.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            direction = direction.normalize()
        self.velocity = direction * BULLET_SPEED

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    """Снаряд, выпущенный врагом."""

    def __init__(self, x, y, target_x, target_y, speed=6):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        direction = pygame.math.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            direction = direction.normalize()
        self.velocity = direction * speed

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()


# --------------------- ВРАГ БЛИЖНЕГО БОЯ --------------------------------
class MeleeEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

        # Ближняя атака
        self.melee_range = 60
        self.melee_damage = 20
        self.attack_cooldown = 1500  # мс
        self.last_attack_time = 0

        self.speed = 2

    def distance_to(self, player):
        return pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        ).length()

    def move_towards(self, player):
        direction = pygame.math.Vector2(
            player.rect.x - self.rect.x,
            player.rect.y - self.rect.y
        )
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def try_melee_attack(self, player):
        dist = self.distance_to(player)
        current_time = pygame.time.get_ticks()

        if dist < self.melee_range:
            if current_time - self.last_attack_time >= self.attack_cooldown:
                player.health -= self.melee_damage
                self.last_attack_time = current_time
                print("MeleeEnemy атакует! HP игрока:", player.health)

    def update(self, player):
        self.move_towards(player)
        self.try_melee_attack(player)


# --------------------- ВРАГ ДАЛЬНЕГО БОЯ --------------------------------
class RangedEnemy(pygame.sprite.Sprite):
    """
    Если игрок слишком близко (< min_distance) – отходим.
    Если игрок слишком далеко (> max_distance) – приближаемся.
    Если в диапазоне [min_distance, max_distance], стреляем.
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((200, 100, 0))  # оранжевый, чтобы отличался
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

        # “Рабочее” окно стрельбы
        self.min_distance = 150  # если игрок ближе, отходим
        self.max_distance = 350  # если игрок дальше, приближаемся
        self.shot_cooldown = 1200  # мс
        self.last_shot_time = 0
        self.speed = 2

    def distance_to(self, player):
        return pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        ).length()

    def move_away_from(self, player):
        direction = pygame.math.Vector2(
            self.rect.centerx - player.rect.centerx,
            self.rect.centery - player.rect.centery
        )
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def move_towards(self, player):
        direction = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def try_shoot(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            self.last_shot_time = current_time
            bullet = EnemyBullet(
                self.rect.centerx, self.rect.centery,
                player.rect.centerx, player.rect.centery,
                speed=6
            )
            enemy_bullets.add(bullet)
            print("RangedEnemy выстрелил!")

    def update(self, player):
        dist = self.distance_to(player)

        if dist < self.min_distance:
            # Игрок слишком близко – отходим
            self.move_away_from(player)
        elif dist > self.max_distance:
            # Игрок слишком далеко – приближаемся
            self.move_towards(player)
        else:
            # Если мы в “золотой середине”, просто стоим (либо можно немного блуждать)
            # и стреляем по кулдауну
            self.try_shoot(player)

        # Делаем ограничение по экрану, чтобы враг не вышел за границы
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


# --------------------------------------------------------------------- #
#                       СОЗДАНИЕ ГРУПП ОБЪЕКТОВ                         #
# --------------------------------------------------------------------- #

player = Player()
player_group = pygame.sprite.Group(player)

bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()


# --------------------------------------------------------------------- #
#                       МЕНЮ И СИСТЕМНЫЕ ФУНКЦИИ                        #
# --------------------------------------------------------------------- #

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
        screen.fill(BLACK)
        title = font.render("Main Menu", True, WHITE)
        play_button = font.render("Play", True, WHITE)
        settings_button = font.render("Settings", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(play_button, (SCREEN_WIDTH // 2 - play_button.get_width() // 2, 200))
        screen.blit(settings_button, (SCREEN_WIDTH // 2 - settings_button.get_width() // 2, 300))
        screen.blit(exit_button, (SCREEN_WIDTH // 2 - exit_button.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_button.get_rect(center=(SCREEN_WIDTH // 2, 200)).collidepoint(mouse_x, mouse_y):
                    return
                if settings_button.get_rect(center=(SCREEN_WIDTH // 2, 300)).collidepoint(mouse_x, mouse_y):
                    settings_menu()
                if exit_button.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
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
        screen.fill(BLACK)
        pause_text = font.render("Paused", True, WHITE)
        resume_button = font.render("Resume", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 200))
        screen.blit(resume_button, (SCREEN_WIDTH // 2 - resume_button.get_width() // 2, 300))
        screen.blit(exit_button, (SCREEN_WIDTH // 2 - exit_button.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if resume_button.get_rect(center=(SCREEN_WIDTH // 2, 300)).collidepoint(mouse_x, mouse_y):
                    return
                if exit_button.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()


def reset_game():
    global player, player_group, bullets, enemies, enemy_bullets, last_shot_time
    player = Player()
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    last_shot_time = 0


def next_wave():
    global wave_active, enemies_to_spawn, enemies_killed
    wave_active = True
    enemies_to_spawn += 2
    enemies_killed = 0


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

        # Клик V - нов
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v and not wave_active:
                next_wave()

        # Спавн врагов
        if wave_active:
            current_time = pygame.time.get_ticks()
            if current_time - spawn_timer > spawn_interval:
                spawn_timer = current_time
                # С вероятностью 50% спавним ближнего, 50% дальнего
                if random.random() < 0.5:
                    enemies.add(MeleeEnemy())
                else:
                    enemies.add(RangedEnemy())

        if wave_active and enemies_killed >= enemies_to_spawn:
            print("Волна закончена")
            wave_active = False

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
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, bullets, True):
            enemies_killed += 1
            enemy.kill()

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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
