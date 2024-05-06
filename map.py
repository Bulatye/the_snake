from constants import *
import pygame

class GameField:
    """Класс, представляющий игровое поле.

    Этот класс инициализирует игровое поле с заданными шириной и высотой.

    Атрибуты:
        field (list): Список координат клеток игрового поля.
        matrix (list): Двумерный массив, представляющий игровое поле.

    Методы:
        __init__(self, width, height): Инициализирует объект игрового поля с заданными размерами.
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
        rect = (SCREEN_HEIGHT, SCREEN_HEIGHT, 1, 1)
        count = 0
        for distance in range(0, SCREEN_WIDTH+30, GRID_SIZE):
            pygame.draw.line(screen, BORDER_COLOR, [distance, 0], [distance, SCREEN_HEIGHT], 3)
            count += 1

        count = 0
        for distance in range(0, SCREEN_HEIGHT+30, GRID_SIZE):
            pygame.draw.line(screen, CYAN, [0, distance], [SCREEN_WIDTH, distance], 3)
            count += 1
