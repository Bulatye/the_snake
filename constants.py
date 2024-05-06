# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
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
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный
CYAN = (93, 216, 228)        # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)            # Цвет яблока
SNAKE_COLOR = (93, 216, 228)         # Цвет змейки

# Скорость движения змейки:
SPEED = 15