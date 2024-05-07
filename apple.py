import pygame
from random import randint

from game_object import GameObject
from constants import (
    GRID_SIZE,
    FIELD_WIDTH,
    FIELD_HEIGHT,
    YELLOW_COLOR_1,
    YELLOW_COLOR_2,
    YELLOW_COLOR_3,
)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре.

    Этот класс отвечает за логику и отображение яблока на игровом поле.

    Атрибуты:
        color (tuple): Цвет яблока в формате RGB.
        position (tuple): Координаты положения яблока на игровом поле.
        game_field (list): Двумерный массив, представляющий игровое поле.

    Методы:
        __init__(snake_positions, Field):
        Инициализирует объект яблока и устанавливает его начальное положение.
        randomize_position(snake_positions):
        Генерирует случайное положение яблока на игровом поле.
        draw(screen): Отрисовывает яблоко на экране игры.
    """

    def __init__(self, snake_positions, field):
        """Инициализирует объект и устанавливает начальное положение яблока.

        Args:
            snake_positions (list): Координаты змеи на игровом поле.
            Field (object): Объект поля игры.
        """
        self.position = self.randomize_position(snake_positions)
        self.game_field = field.field
        self.body_color = [YELLOW_COLOR_1, YELLOW_COLOR_2, YELLOW_COLOR_3]

    def randomize_position(self, snake_positions):
        """Генерирует случайные координаты яблока на игровом поле.

        Args:
            snake_positions (list): Координаты змеи на игровом поле.

        Returns:
            tuple: Координаты яблока на игровом поле.
        """
        apple_x = randint(0, FIELD_WIDTH - 1)
        apple_y = randint(0, FIELD_HEIGHT - 1)

        while (apple_x, apple_y) in snake_positions:
            apple_x = randint(0, FIELD_WIDTH - 1)
            apple_y = randint(0, FIELD_HEIGHT - 1)

        return (apple_x, apple_y)

    def draw(self, screen, animation_tic):
        """Отрисовывает яблоко на экране игры.
        Реализована анимация, каждые три кадра
        чередуются сущетсвующие цвета.

        Args:
            screen (pygame.Surface): Экран игры.
            animation_tic (int): Кадр анимации.
        """
        cell = self.game_field[self.position[0]][self.position[1]]
        rect = pygame.Rect(cell, (GRID_SIZE + 1, GRID_SIZE + 1))
        pygame.draw.rect(screen, self.body_color[animation_tic], rect)
