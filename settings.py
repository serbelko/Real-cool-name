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
spawn_interval = 2

PLAYER_MAX_HEALTH = 1000000000