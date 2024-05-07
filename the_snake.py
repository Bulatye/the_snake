import threading
import pygame
import os

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPEED,
    BACKGROUND,
    CYAN,
    YELLOW_COLOR_1,
    YELLOW_COLOR_2,
    YELLOW_COLOR_3,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    FIELD_WIDTH,
    FIELD_HEIGHT,
)
from map import GameField
from snake import Snake
from apple import Apple

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('SNAKEEEE')
# Настройка времени:
clock = pygame.time.Clock()


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
    font_size_h4 = 32

    running = True

    colors = [YELLOW_COLOR_1, YELLOW_COLOR_2, YELLOW_COLOR_3]
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
            if not self.snake.check_snake_clash():
                self.view_death_screen()
            else:
                # Управление частотой кадров:
                clock.tick(SPEED)
                # Очистка экрана:
                screen.fill(BACKGROUND)
                # Отрисвока имени и рекорда
                self.view_name_and_score()
                # Отрисовка змейки:
                self.snake.draw(screen)
                # Проверка столкновения змейки с яблоком:
                if self.snake.check_apple_clash(self.apple.position):
                    # Получение нового яблока:
                    self.apple = Apple(self.snake.positions, self.field)
                    screen.fill(CYAN)
                    self.score += 1

                # Отрисовка сетки:
                self.field.draw_grid(screen)
                # Отрисовка яблока c анимацией:
                if self.apple_animation_tic > 2:
                    self.apple_animation_tic = 0

                self.apple.draw(screen, self.colors[self.apple_animation_tic])
                self.apple_animation_tic += 1

                # Обновление направления движения змейки:
                self.snake.update_direction()
                # Обновление экрана:
                pygame.display.update()

        # Завершение игры:
        pygame.quit()

    def event_listener(self):
        """Функция для прослушивания событий клавиатуры в отдельном потоке.
        Это необходимо для получения наивысшей отзывчивости змеи.
        """
        while self.running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.snake.direction != DOWN:
                self.snake.next_direction = UP
            elif keys[pygame.K_DOWN] and self.snake.direction != UP:
                self.snake.next_direction = DOWN
            elif keys[pygame.K_LEFT] and self.snake.direction != RIGHT:
                self.snake.next_direction = LEFT
            elif keys[pygame.K_RIGHT] and self.snake.direction != LEFT:
                self.snake.next_direction = RIGHT

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
                self.snake.reset()
                self.score = 0

    def view_name_and_score(self):
        """Функция для отображения имени игрока и текущего счета."""
        # Создание объектов текста
        font_score = pygame.font.Font(self.font, self.font_size_h4)
        font_nickname = pygame.font.Font(self.font, self.font_size_h4)

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


if __name__ == '__main__':
    # Создание объекта игры и запуск основной функции:
    game = Game()
    input_thread = threading.Thread(target=game.event_listener)
    input_thread.start()
    game.main()
