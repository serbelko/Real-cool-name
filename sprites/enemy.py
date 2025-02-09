import pygame
from  settings import *
import random
from .weapon import EnemyBullet
enemy_bullets = pygame.sprite.Group()

class MeleeEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Коэффициент увеличения (2x)
        self.scale_factor = 4

        # Загрузка анимаций (только вправо и влево)
        self.animations = {
            "right": [self.load_and_scale(f"assetspngs/melee/melee_right_{i}.png") for i in range(9)],
            "left": [self.load_and_scale(f"assetspngs/melee/melee_left_{i}.png") for i in range(9)]
        }

        # Начальные параметры
        self.image = self.animations["right"][0]  # Начальное изображение
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

        # Ближняя атака
        self.melee_range = 60
        self.melee_damage = 20
        self.attack_cooldown = 1500  # мс
        self.last_attack_time = 0
        self.hp = 15
        self.speed = 2

        # Анимация
        self.current_frame = 0
        self.frame_rate = 150  # Скорость анимации (мс)
        self.last_update = pygame.time.get_ticks()
        self.direction = "right"  # Начальное направление

        

    def load_and_scale(self, path):
        """Загружает и увеличивает изображение в 2 раза"""
        img = pygame.image.load(path).convert_alpha()
        new_size = (img.get_width() * self.scale_factor, img.get_height() * self.scale_factor)
        return pygame.transform.scale(img, new_size)

        

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

            # Используем "right" и "left" даже при движении вверх и вниз
            self.direction = "right" if direction.x > 0 else "left"

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

    def update_animation(self):
        """Обновляет анимацию движения"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations["right"])
            self.image = self.animations[self.direction][self.current_frame]

    def update(self, player):
        self.move_towards(player)
        self.try_melee_attack(player)
        self.update_animation()



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
        self.hp = 20

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
