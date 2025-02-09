import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Коэффициент увеличения (например, 2x)
        self.scale_factor = 4

        # Загрузка и масштабирование анимаций
        self.animations = {
            "down": [self.load_and_scale(f"sprites/user/down_{i}.png") for i in range(7)],
            "up": [self.load_and_scale(f"sprites/user/up_{i}.png") for i in range(7)],
            "left": [self.load_and_scale(f"sprites/user/left_{i}.png") for i in range(7)],
            "right": [self.load_and_scale(f"sprites/user/right_{i}.png") for i in range(7)]
        }

        # Начальное изображение
        self.image = self.animations["down"][0]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Переменные состояния
        self.weapon = 'gun'
        self.is_attacking = False
        self.last_attack_time = 0
        self.attack_rect = pygame.Rect(0, 0, HITBOX_WIDTH, HITBOX_HEIGHT)
        self.direction = 'down'
        self.health = PLAYER_MAX_HEALTH
        self.speed = PLAYER_SPEED
        self.currency = 0
        self.skills = {}

        # Анимация
        self.current_frame = 0
        self.frame_rate = 100  # Скорость анимации (мс)
        self.last_update = pygame.time.get_ticks()

    def load_and_scale(self, path):
        """ Загружает и увеличивает изображение """
        img = pygame.image.load(path).convert_alpha()
        new_size = (img.get_width() * self.scale_factor, img.get_height() * self.scale_factor)
        return pygame.transform.scale(img, new_size)


    def add_currency(self, amount):
        self.currency += amount

    def spend_currency(self, cost):
        if self.currency >= cost:
            self.currency -= cost
            return True
        return False

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

    def update_animation(self, attacking=False):
        """Обновляет кадры анимации."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.direction])
            if attacking:
                self.image = self.animations[f"attack_{self.direction}"][self.current_frame]
            else:
                self.image = self.animations[self.direction][self.current_frame]

    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_w] and self.rect.top > 0:
            dy -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            dy += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            dx -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            dx += self.speed

        self.rect.x += dx
        self.rect.y += dy

        if dx != 0 or dy != 0:
            self.update_direction(dx, dy)
            self.update_animation()  # Запускаем анимацию при движении
        else:
            self.image = self.animations[self.direction][0]  # Статичное изображение

    def start_melee_attack(self):
        """Запуск атаки ближнего боя."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= ATTACK_COOLDOWN:
            self.is_attacking = True
            self.last_attack_time = current_time
            self.current_frame = 0  # Начинаем анимацию атаки сначала

    def update_melee_attack(self, enemies_group):
        """Обновляет атаку ближнего боя."""
        if not self.is_attacking:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > ATTACK_DURATION:
            self.is_attacking = False
            return

        # Включаем анимацию атаки
        self.update_animation(attacking=True)

        # Определяем область удара
        if self.direction == 'up':
            self.attack_rect.size = (HITBOX_WIDTH, HITBOX_HEIGHT)
            self.attack_rect.midbottom = self.rect.midtop
        elif self.direction == 'down':
            self.attack_rect.size = (HITBOX_WIDTH, HITBOX_HEIGHT)
            self.attack_rect.midtop = self.rect.midbottom
        elif self.direction == 'left':
            self.attack_rect.size = (HITBOX_HEIGHT, HITBOX_WIDTH)
            self.attack_rect.midright = self.rect.midleft
        elif self.direction == 'right':
            self.attack_rect.size = (HITBOX_HEIGHT, HITBOX_WIDTH)
            self.attack_rect.midleft = self.rect.midright

        # Проверяем попадание по врагам
        for enemy in enemies_group:
            if self.attack_rect.colliderect(enemy.rect):
                enemy.kill()
