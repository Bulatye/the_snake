import pygame
from constants import *

class Snake():
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
        check_apple_clash(apple_position): Проверяет столкновение змеи с яблоком.
        check_snake_clash(): Проверяет столкновение змеи с самой собой.
        reset(): Сбрасывает состояние змеи до начального.

    """

    direction = UP
    next_direction = None
    color = SNAKE_COLOR

    def __init__(self, snake, field):
        """Инициализирует объект и устанавливает начальное положение змеи на поле.

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
        Отрисовывает тело змеи, голову с учетом ее направления, затирает ее хвост.
        Создает движение змеи.
        """
        # Отрисовка змеи
        for position in self.positions:
            cell = self.game_field[position[0]][position[1]]
            rect = pygame.Rect(cell, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color, rect)

        # Обработка события, если змейка достигла края окна
        snake_head_now = self.positions[0]

        if snake_head_now[1] == FIELD_HEIGHT and self.direction == DOWN:
            self.positions[0][1] = 0
        elif snake_head_now[1] == 0 and self.direction == UP:
            self.positions[0][1] = FIELD_HEIGHT

        if snake_head_now[0] == FIELD_WIDTH - 1 and self.direction == RIGHT:
            self.positions[0][0] = 0
        elif snake_head_now[0] == 0 and self.direction == LEFT:
            self.positions[0][0] = FIELD_WIDTH - 1

        # Создание координат следующей ячейки
        next_cell = [self.positions[0][0] + self.direction[0], self.positions[0][1] + self.direction[1]]
        self.positions.insert(0, next_cell)

        # Рисование головы змеи
        snake_head = self.game_field[self.positions[0][0]][self.positions[0][1]]
        head_rect = pygame.Rect(snake_head, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, head_rect)

        # Затирание последнего сегмента
        snake_tail = self.game_field[self.positions[-1][0]][self.positions[-1][1]]
        last_rect = pygame.Rect(snake_tail, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BACKGROUND, last_rect)

        # Удаление хвоста змеи из массива
        self.positions.pop(-1)

    def check_apple_clash(self, apple_position):
        """Возвращает True, если голова змеи столкнулась с яблоком."""
        if tuple(self.positions[0]) == apple_position:
            self.positions.append(self.positions[-1] + list(self.direction))
            return True

    def check_snake_clash(self):
        """Сбрасывает змею, если ее голова столкнулась с ее телом."""
        for i in range(1, len(self.positions)):
            if self.positions[0] == self.positions[i]:
                return False
        return True

    def reset(self):
        """Сбрасывает змею, устанавливая ее в начальное состояние."""
        body_snake = [[16, 12], [16, 11], [16, 10]]
        self.positions = body_snake
        self.next_direction = None
