import threading
import pygame
import os
from abc import ABC, abstractmethod

from map import GameField
from snake import Snake
from apple import Apple

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 642, 482
FIELD_WIDTH = 32
FIELD_HEIGHT = 23
# Скорость движения змейки:
SPEED = 15
# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный
CYAN = (111, 235, 247)  # Цвет границы ячейки
YELLOW_COLOR_3 = (245, 250, 80)  # Цвет яблока 3
BACKGROUND = (0, 0, 0)
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('SNAKEEEE')
# Настройка времени:
clock = pygame.time.Clock()


class GameObject(ABC):
    """Класс, представляющий игровой объект."""

    self.position = (0, 0)
    self.body_color = None

    def __init__(self):
        """Инициализирует базовые атрибуты игрового объекта."""
        pass

    def draw(self):
        """
        Абстрактный метод,
        который должен быть переопределен в дочерни хклассах.
        Этот метод определяет, как объект будет отображаться на экране.
        По умолчанию он ничего не делает.
        """
        pass


class Game:
    """Класс, представляющий игру "Змейка".

    Этот класс обеспечивает основную логику игры.

    Attributes:
        screen: Объект экрана Pygame.
        clock: Объект Pygame Clock, используемый для управления скоростью игры.
        field: Объект игрового поля.
        snake: Объект змейки.
        apple: Объект яблока.
        font_path: Путь к файлу шрифта.
        font_size_h1: Размер шрифта для заголовка 1.
        font_size_h2: Размер шрифта для заголовка 2.
        font_size_footer_text: Размер шрифта для текста в нижнем колонтитуле.
        running: Флаг для указания состояния игры (запущена или завершена).
        colors: Список цветов для анимации яблока.
        apple_animation_tic: Переменная для анимации яблока.
        score: Очки игрока.
        nickname: Никнейм игрока.

    Methods:
        __init__(): Инициализация игры.
        main(): Основная функция игры.
        event_listener(): Функция для прослушивания событий клавиатуры.
        view_death_screen(): Функция для отображения экрана смерти.
        view_name_and_score():
        Функция для отображения имени игрока и текущего счета.
    """

    font = os.path.join("fonts", "8bitOperatorPlus8-Regular.ttf")
    font_size_h1 = 72
    font_size_h2 = 24
    font_size_footer_text = 32

    running = True

    apple_animation_tic = 0

    score = 0
    nickname = "bulatue"

    def __init__(self):
        """Инициализация игры."""
        # Инициализация PyGame:
        pygame.init()
        # Создание объекта игрового поля:
        self.field = GameField(FIELD_WIDTH, FIELD_HEIGHT)
        # Создание объекта змейки:
        self.snake = Snake([[16, 10], [16, 11], [16, 12]], self.field.field)
        # Создание объекта яблока:
        self.apple = Apple(self.snake.positions, self.field)

    def main(self):
        """Основная функция игры."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Проверка столкновения змейки с самой собой:
            if not self.snake.check_snake_collision():
                self.view_death_screen()
            else:
                # Управление частотой кадров:
                clock.tick(SPEED)
                # Очистка экрана:
                screen.fill(BACKGROUND)
                # Отрисвока имени и рекорда
                self.view_name_and_score()
                # Двигаем змейку
                self.snake.move(screen)
                # Отрисовка змейки:
                self.snake.draw(screen)
                # Проверка столкновения змейки с яблоком:
                if self.snake.check_apple_collision(self.apple.position):
                    # Получение нового яблока:
                    self.apple = Apple(self.snake.positions, self.field)
                    screen.fill(CYAN)
                    self.score += 1

                # Отрисовка сетки:
                self.field.draw_grid(screen)
                # Отрисовка яблока c анимацией:
                if self.apple_animation_tic > 2:
                    self.apple_animation_tic = 0

                self.apple.draw(screen, self.apple_animation_tic)
                self.apple_animation_tic += 1

                # Обновление направления движения змейки:
                self.snake.update_direction()
                # Обновление экрана:
                pygame.display.update()

        # Завершение игры:
        pygame.quit()

    def view_death_screen(self):
        """Функция для отображения экрана смерти."""
        # Отчищаем экран.
        screen.fill(BACKGROUND)
        # Уведомляем пользователя о его смерти.
        # Спрашиваем хочет ли он начать сначала.

        # Создание объектов текста
        font_you_died = pygame.font.Font(self.font, self.font_size_h1)
        font_press_r = pygame.font.Font(self.font, self.font_size_h2)

        str_h1 = "YOU DIED"
        str_h2 = "Press R to Restart"
        text_you_died = font_you_died.render(str_h1, True, CYAN)
        text_press_r = font_press_r.render(str_h2, True, YELLOW_COLOR_3)

        # Центральные координаты текста оповещающем о смерти:
        text_width, text_height = font_you_died.size("YOU DIED")

        x = (SCREEN_WIDTH - text_width) // 2
        y = ((SCREEN_HEIGHT + 100) - text_height * 2) // 2
        DEATH_TEXT_CENTER = x, y
        # Прорисовка текста оповещающем о смерти.
        screen.blit(text_you_died, DEATH_TEXT_CENTER)

        # Центральные координаты текста с просьбой перезапуска:
        text_width, text_height = font_press_r.size("Press R to restart")

        x = (SCREEN_WIDTH - text_width) // 2
        y = ((SCREEN_HEIGHT + 100) + text_height) // 2
        PRESS_R_TEXT_CENTER = x, y
        # Прорисовка текста оповещающем о смерти.
        screen.blit(text_press_r, PRESS_R_TEXT_CENTER)
        # обновляем экран
        pygame.display.update()

        # Прослушиваем событие нажатия кнопки R
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                self.running = False
            elif keys[pygame.K_r]:
                # Перезапускаем игру
                self.score = 0
                self.snake.next_direction = UP
                self.snake.reset()

    def view_name_and_score(self):
        """Функция для отображения имени игрока и текущего счета."""
        # Создание объектов текста
        font_score = pygame.font.Font(self.font, self.font_size_h2)
        font_nickname = pygame.font.Font(self.font, self.font_size_h2)

        text_score = font_score.render(str(self.score), True, YELLOW_COLOR_3)
        text_nickname = font_nickname.render(self.nickname, True, CYAN)

        # Центральные координаты текста оповещающем о смерти:
        text_width, text_height = font_score.size("YOU DIED")

        TEXT_SCORE = SCREEN_WIDTH - 60, SCREEN_HEIGHT + 40
        # Прорисовка текста оповещающем о смерти.
        screen.blit(text_score, TEXT_SCORE)

        # Центральные координаты текста с просьбой перезапуска:
        text_width, text_height = font_nickname.size("Press R to restart")

        TEXT_NICKNAME = 30, SCREEN_HEIGHT + 40
        screen.blit(text_nickname, TEXT_NICKNAME)


def handle_keys(game):
    """Функция для прослушивания событий клавиатуры в отдельном потоке.
    Это необходимо для получения наивысшей отзывчивости змеи.
    """
    while game.running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and game.snake.direction != DOWN:
            game.snake.next_direction = UP
        elif keys[pygame.K_DOWN] and game.snake.direction != UP:
            game.snake.next_direction = DOWN
        elif keys[pygame.K_LEFT] and game.snake.direction != RIGHT:
            game.snake.next_direction = LEFT
        elif keys[pygame.K_RIGHT] and game.snake.direction != LEFT:
            game.snake.next_direction = RIGHT


def main():
    """Запуск потоков игры."""
    # Создание объекта игры и запуск основной функции:
    game = Game()
    input_thread = threading.Thread(target=handle_keys, args=(game,))
    input_thread.start()
    game.main()


if __name__ == '__main__':
    main()
