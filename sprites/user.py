import pygame
from settings import *



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

        # скорость
        self.speed = PLAYER_SPEED

        # Кошелек
        self.currency = 0

        # Скиллы
        self.skills = {}

        self.strength = 5

    def add_currency(self, amount):
        self.currency += amount

    def spend_currency(cost):
        global player_currency
        if player_currency >= cost:
            player_currency -= cost
            return True
        else:
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