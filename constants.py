# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 642, 482
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BACKGROUND = (0, 0, 0)

FIELD_WIDTH = 32
FIELD_HEIGHT = 24

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0) # Цвет фона - черный
CYAN = (93, 216, 228) # Цвет границы ячейки
APPLE_COLOR_1 = (243, 250, 17) # Цвет яблока 1
APPLE_COLOR_2 = (211, 217, 15) # Цвет яблока 2
APPLE_COLOR_3 = (245, 250, 80) # Цвет яблока 3
SNAKE_COLOR = (93, 216, 228) # Цвет змейки

# Скорость движения змейки:
SPEED = 15