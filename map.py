from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_SIZE,
    CYAN,
    FIELD_WIDTH,
    FIELD_HEIGHT,
)
import pygame


from abc import ABC, abstractmethod


class GameObject(ABC):
    """Класс, представляющий игровой объект."""

    def __init__(self):
        """Инициализирует базовые атрибуты игрового объекта."""
        # Позиция объекта на игровом поле (инициализирована как центр экрана)
        self.position = (0, 0)
        # Цвет объекта (не определен явно в классе GameObject)
        self.body_color = None

    @abstractmethod
    def draw(self):
        """
        Абстрактный метод,
        который должен быть переопределен в дочерни хклассах.
        Этот метод определяет, как объект будет отображаться на экране.
        По умолчанию он ничего не делает.
        """
        pass


class GameField:
    """Класс, представляющий игровое поле.
    Этот класс инициализирует игровое поле с заданными шириной и высотой.

    Атрибуты:
        field (list): Список координат клеток игрового поля.
        matrix (list): Двумерный массив, представляющий игровое поле.

    Методы:
        __init__(self, width, height):
        Инициализирует объект игрового поля с заданными размерами.
        draw_grid(screen): Рисует сетку на игровом поле.

    """

    def __init__(self, width, height):
        """Инициализирует объект игрового поля с заданными размерами.

        Args:
            width (int): Ширина игрового поля.
            height (int): Высота игрового поля.
        """
        self.field = list()
        self.matrix = list()

        for i in range(0, FIELD_WIDTH):
            row_field = list()
            row_matrix = list()
            for j in range(0, FIELD_HEIGHT + 1):
                row_field.append(((i * 20), (j * 20)))
                row_matrix.append((i, j))

            self.field.append(row_field)
            self.matrix.append(row_matrix)

    def draw_grid(self, screen):
        """Рисует сетку на игровом поле

        Args:
            screen (pygame.Surface): Экран игры.
        """
        count = 0
        for distance in range(0, SCREEN_WIDTH + 30, GRID_SIZE):
            x = [distance, 0]
            y = [distance, SCREEN_HEIGHT]
            pygame.draw.line(screen, CYAN, x, y, 3)
            count += 1

        count = 0
        for distance in range(0, SCREEN_HEIGHT, GRID_SIZE):
            x = [0, distance]
            y = [SCREEN_WIDTH, distance]
            pygame.draw.line(screen, CYAN, x, y, 3)
            count += 1
