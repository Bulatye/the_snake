import pygame

from gameobject import GameObject
from constants import (
    BACKGROUND,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    FIELD_WIDTH,
    FIELD_HEIGHT,
    SNAKE_COLOR,
    GRID_SIZE
)


class Snake(GameObject):
    """Класс, представляющий змею в игре.

    Этот класс обеспечивает логику и поведение змеи в игровом мире.

    Атрибуты:
        direction (tuple): Текущее направление движения змеи.
        next_direction (tuple): Следующее направление движения змеи.
        color (tuple): Цвет змеи в формате RGB.
        positions (list): Список координат сегментов змеи на игровом поле.
        game_field (list): Двумерный массив, представляющий игровое поле.

    Методы:
        update_direction(): Обновляет текущее направление змеи.
        draw(screen): Отрисовывает змею на экране игры.
        check_apple_clash(apple_position):
        Проверяет столкновение змеи с яблоком.
        check_snake_clash(): Проверяет столкновение змеи с самой собой.
        reset(): Сбрасывает состояние змеи до начального.

    """

    direction = UP
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self, snake, field):
        """Инициализирует объект и устанавливает
        начальное положение змеи на поле.

        Args:
            snake (list): Начальное положение змеи на поле.
            field (list): Игровое поле, полезно для отрисовки змеи.
        """
        self.positions = list(snake)
        self.game_field = field

    def update_direction(self):
        """Обновляет направление змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, screen):
        """Основной метод змеи.
        Отрисовывает тело змеи.
        """
        # Получаем координаты головы змеи.
        x_head, y_head = self.get_head_position()
        # Отрисовка змеи
        for position in self.positions:
            x_body, y_body = position[0], position[1]

            cell = self.game_field[x_body][y_body]
            rect = pygame.Rect(cell, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)

    def move(self, screen):
        """Основной метод змеи.
        Отрисовывает голову с учетом ее направления, затирает хвост.
        Создает движение змеи.
        """
        # Обработка события, если змейка достигла края окнаs
        x_head, y_head = self.get_head_position()
        if y_head == FIELD_HEIGHT and self.direction == DOWN:
            self.positions[0][1] = 0
            print(self.positions[0][1])
        elif y_head == 0 and self.direction == UP:
            self.positions[0][1] = FIELD_HEIGHT

        if x_head == FIELD_WIDTH - 1 and self.direction == RIGHT:
            self.positions[0][0] = 0
        elif x_head == 0 and self.direction == LEFT:
            self.positions[0][0] = FIELD_WIDTH - 1

        x_head, y_head = self.get_head_position()
        # Создание координат следующей ячейки
        x_next = x_head + self.direction[0]
        y_next = y_head + self.direction[1]
        self.positions.insert(0, [x_next, y_next])

        # Рисование головы змеи
        snake_head = self.game_field[x_head][y_head]
        head_rect = pygame.Rect(snake_head, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)

        # Затирание последнего сегмента
        x_tail, y_tail = self.get_tail_position()
        snake_tail = self.game_field[x_tail][y_tail]
        last_rect = pygame.Rect(snake_tail, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BACKGROUND, last_rect)

        # Удаление хвоста змеи из массива
        self.positions.pop(-1)

    def get_head_position(self):
        """Возращает позицию головы змеи."""
        x_head = self.positions[0][0]
        y_head = self.positions[0][1]
        return x_head, y_head

    def get_tail_position(self):
        """Возращает позицию хвоста змеи."""
        x_tail = self.positions[-1][0]
        y_tail = self.positions[-1][1]
        return x_tail, y_tail

    def check_apple_collision(self, apple_position):
        """Возвращает True, если голова змеи столкнулась с яблоком."""
        if tuple(self.positions[0]) == apple_position:
            self.positions.append(self.positions[-1] + list(self.direction))
            self.positions.append(self.positions[-1] + list(self.direction))
            return True

    def check_snake_collision(self):
        """Сбрасывает змею, если ее голова столкнулась с ее телом."""
        for i in range(1, len(self.positions)):
            if self.positions[0] == self.positions[i]:
                return False
        return True

    def reset(self):
        """Сбрасывает змею, устанавливая ее в начальное состояние."""
        body_snake = [[16, 10], [16, 11], [16, 12]]
        self.positions = body_snake
        self.next_direction = None
