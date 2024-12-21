import pygame
import random
import sys

pygame.init()

# Константы
SCREEN_WIDTH = 800  # Ширина окна игры
SCREEN_HEIGHT = 600  # Высота окна игры
WHITE = (255, 255, 255)  # Цвет для пуль
BLACK = (0, 0, 0)  # Цвет фона
RED = (255, 0, 0)  # Цвет врагов
BLUE = (0, 0, 255)  # Цвет игрока
PLAYER_SPEED = 5  # Скорость движения игрока
BULLET_SPEED = 10  # Скорость пуль
ENEMY_SPEED = 2  # Скорость врагов
RELOAD_DELAY = 200  # Задержка между выстрелами в миллисекундах

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Real Cool name")  # Заголовок окна игры

# Шрифты
font = pygame.font.Font(None, 36)  # Шрифт для текста

# Таймер
clock = pygame.time.Clock()  # Таймер для контроля FPS
last_shot_time = 0  # Отслеживание времени последнего выстрела

# Классы
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Представление игрока
        self.image.fill(BLUE)  # Заливка игрока синим цветом
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Начальная позиция игрока

    def update(self, keys):
        dx, dy = 0, 0  # Изменение координат
        if keys[pygame.K_w] and self.rect.top > 0:  # Движение вверх
            dy -= PLAYER_SPEED
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:  # Движение вниз
            dy += PLAYER_SPEED
        if keys[pygame.K_a] and self.rect.left > 0:  # Движение влево
            dx -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:  # Движение вправо
            dx += PLAYER_SPEED
        self.rect.x += dx
        self.rect.y += dy  # Применение изменения координат

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Представление пули
        self.image.fill(WHITE)  # Заливка пули белым цветом
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(target_x - x, target_y - y).normalize() * BULLET_SPEED  # Направление и скорость

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        # Удаление пули, если она выходит за пределы экрана
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Представление врага
        self.image.fill(RED)  # Заливка врага красным цветом
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  # Случайное начальное положение
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

    def update(self, player):
        # Движение к игроку
        direction = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y).normalize()
        self.rect.x += direction.x * ENEMY_SPEED
        self.rect.y += direction.y * ENEMY_SPEED

# Группы для игровых объектов
player = Player()
player_group = pygame.sprite.Group(player)

bullets = pygame.sprite.Group()  # Группа для управления всеми пулями
enemies = pygame.sprite.Group()  # Группа для управления всеми врагами

# Функции
def main_menu():
    """Отображение главного меню и обработка взаимодействий."""
    while True:
        screen.fill(BLACK)
        title = font.render("Main Menu", True, WHITE)
        play_button = font.render("Play", True, WHITE)
        settings_button = font.render("Settings", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        # Отрисовка кнопок
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
                    return  # Начало игры
                if exit_button.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # Выход из игры

def game_over():
    """Отображение экрана окончания игры и обработка взаимодействий."""
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        reload_button = font.render("Reload Game", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        # Отрисовка кнопок
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
                    return True  # Перезапуск игры
                if exit_button.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # Выход из игры
    return False

def pause_menu():
    """Отображение меню паузы и обработка взаимодействий."""
    while True:
        screen.fill(BLACK)
        pause_text = font.render("Paused", True, WHITE)
        resume_button = font.render("Resume", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        # Отрисовка кнопок
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
                    return  # Возобновление игры
                if exit_button.get_rect(center=(SCREEN_WIDTH // 2, 400)).collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # Выход из игры

# Основной игровой цикл
def reset_game():
    """Сброс состояния игры для новой сессии."""
    global player, player_group, bullets, enemies
    player = Player()
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

main_menu()

spawn_enemy_event = pygame.USEREVENT + 1  # Пользовательское событие для спавна врагов
pygame.time.set_timer(spawn_enemy_event, 2000)  # Спавн врагов каждые 2 секунды

running = True
paused = False
while running:
    keys = pygame.key.get_pressed()  # Получение текущего состояния клавиш
    screen.fill(BLACK)  # Очистка экрана

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Выход из игрового цикла
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > RELOAD_DELAY:  # Учет задержки выстрелов
                last_shot_time = current_time
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y)
                bullets.add(bullet)  # Добавление пули в группу
        if event.type == spawn_enemy_event:
            enemies.add(Enemy())  # Добавление нового врага
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_menu()  # Пауза игры

    player.update(keys)  # Обновление позиции игрока
    bullets.update()  # Обновление пуль
    enemies.update(player)  # Обновление врагов

    # Проверка столкновений
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, bullets, True):
            enemy.kill()  # Уничтожение врага при попадании пули
        if pygame.sprite.collide_rect(enemy, player):
            if game_over():
                reset_game()  # Сброс игры после окончания
            else:
                running = False  # Выход из игрового цикла

    # Отрисовка объектов
    player_group.draw(screen)  # Отрисовка игрока
    bullets.draw(screen)  # Отрисовка пуль
    enemies.draw(screen)  # Отрисовка врагов

    pygame.display.flip()  # Обновление экрана
    clock.tick(60)  # Ограничение FPS до 60

pygame.quit()
