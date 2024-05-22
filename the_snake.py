"""Змейка."""
from random import randint as ri
import pygame as pg

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный
APPLE_COLOR = (248, 76, 21)
SNAKE_COLOR = (0, 175, 80)
CENTER = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

# Скорость движения змейки
SPEED = 15

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('YANDEX SNAKE')
# Настройка времени
clock = pg.time.Clock()


class GameObject:
    """Класс, представляющий игровой объект."""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        """Инициализирует базовые атрибуты игрового объекта."""
        self.position = position if position else CENTER.copy()
        self.body_color = body_color

    def draw_rect(self, screen):
        """Рисует прямоугольник."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)

    def draw(self, screen):
        """Метод для отрисовки объекта на экране."""
        self.draw_rect(screen)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, snake_positions=None, body_color=APPLE_COLOR):
        """Инициализирует объект и устанавливает начальное положение яблока."""
        super().__init__(body_color=body_color)
        self.randomize_position(snake_positions or [])

    def randomize_position(self, snake_positions):
        """Генерирует случайные координаты яблока на игровом поле."""
        while True:
            self.position = (
                ri(0, GRID_WIDTH - 1) * GRID_SIZE,
                ri(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                break


class Snake(GameObject):
    """Класс, представляющий змею в игре."""

    def __init__(self):
        """Инициализирует объект и устанавливает положение змеи на поле."""
        super().__init__(position=CENTER.copy(), body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self, screen):
        """Отрисовывает тело змеи."""
        for position in self.positions:
            self.position = position
            self.draw_rect(screen)

    def move(self):
        """Обновляет координаты змеи в positions."""
        x, y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Обновляет направление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змеи."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змеи до начального."""
        self.length = 1
        self.positions = [CENTER.copy()]
        self.direction = RIGHT
        self.next_direction = None
        self.position = CENTER.copy()


def main():
    """Основная функция игры."""
    running = True 

    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while running:
        clock.tick(SPEED)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        for i in range(1, len(snake.positions)):
            if snake.positions[0] == snake.positions[i]:
                snake.reset()
                apple.randomize_position(snake.positions)
                break

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()

    pg.quit()


def handle_keys(snake):
    """Обработка одиночных нажатий клавиш."""
    keys = pg.key.get_pressed()
    key_actions = {
        pg.K_UP: UP,
        pg.K_DOWN: DOWN,
        pg.K_LEFT: LEFT,
        pg.K_RIGHT: RIGHT,
    }
    for key, direction in key_actions.items():
        if keys[key] and snake.direction != opposite_direction(direction):
            snake.next_direction = direction
            break


def opposite_direction(direction):
    """Возвращает противоположное направление."""
    return {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,
    }[direction]


if __name__ == '__main__':
    main()