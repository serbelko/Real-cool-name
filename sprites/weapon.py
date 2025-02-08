from settings import *
import pygame


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
        self.strenght = 10

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
