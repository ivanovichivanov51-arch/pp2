# config.py

# Экран
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 640  # 40px жоғарыдағы HUD үшін
GRID_SIZE = 20       # Бір ұяшық өлшемі (px)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE   # 30 ұяшық
GRID_HEIGHT = (SCREEN_HEIGHT - 40) // GRID_SIZE  # 30 ұяшық

# FPS (жылдамдық деңгейлері)
BASE_FPS = 8
FPS_INCREMENT = 1    # Әр деңгейде +2

# Түстер (R, G, B)
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (40,  40,  40)
GREEN      = (0,   200, 0)
DARK_GREEN = (0,   140, 0)
RED        = (220, 0,   0)
DARK_RED   = (139, 0,   0)   # Poison food
YELLOW     = (255, 220, 0)   # Speed boost
CYAN       = (0,   220, 220) # Slow motion
PURPLE     = (180, 0,   220) # Shield
ORANGE     = (255, 140, 0)   # Bonus food
BROWN      = (139, 69,  19)  # Obstacle

# Тамақ түрлері
FOOD_NORMAL  = "normal"   # +1 ұпай
FOOD_BONUS   = "bonus"    # +3 ұпай, 5 сек жоғалады
FOOD_POISON  = "poison"   # жылан қысқарады

# Power-up түрлері
PU_SPEED  = "speed"
PU_SLOW   = "slow"
PU_SHIELD = "shield"

# Деңгей прогрессиясы
FOODS_PER_LEVEL = 5   # 5 тамақ жесе — жаңа деңгей

# DB байланыс параметрлері (өз мәліметтеріңді жаз)
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "snake_db",
    "user":     "postgres",
    "password": "sekow102"       
}