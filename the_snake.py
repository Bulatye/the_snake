import threading
import pygame
import os

from constants import *
from map import *
from snake import Snake
from apple import Apple

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')
# Настройка времени:
clock = pygame.time.Clock()


class Game:
    """Класс, представляющий игру "Змейка".

    Этот класс обеспечивает основную логику игры.

    Attributes:
        screen: Объект экрана Pygame, на котором происходит отрисовка игровых объектов.
        clock: Объект Pygame Clock, используемый для управления скоростью игры.
        field: Объект игрового поля.
        snake: Объект змейки.
        apple: Объект яблока.

    Methods:
        main(): Основная функция игры.
        event_listener(): Функция для прослушивания событий клавиатуры в отдельном потоке.
        view_death_screen(): Функция для отображения экрана смерти.
    """

    font_path = os.path.join("fonts", "8bitOperatorPlus8-Regular.ttf")
    font_size_h1 = 72
    font_size_h2 = 24

    running = True

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
                # Отрисовка змейки:
                self.snake.draw(screen)
                # Проверка столкновения змейки с яблоком:
                if self.snake.check_apple_clash(self.apple.position):
                    # Получение нового яблока:
                    self.apple = Apple(self.snake.positions, self.field)
                    screen.fill(CYAN)
                # Отрисовка яблока:
                self.apple.draw(screen)
                # Отрисовка сетки:
                self.field.draw_grid(screen)

                # Обновление направления движения змейки:
                self.snake.update_direction()
                # Обновление экрана:
                pygame.display.update()

        # Завершение игры:
        pygame.quit()

    def event_listener(self):
        """Функция для прослушивания событий клавиатуры в отдельном потоке.
        Это необходимо для получения наивысшей отзывчивости змеи."""
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
        # Отчищаем экран.
        screen.fill(BACKGROUND)
        # Уведомляем пользователя о его смерти.
        # Спрашиваем хочет ли он начать сначала.

        # Создание объектов текста
        font_you_died = pygame.font.Font(self.font_path, self.font_size_h1)
        font_press_r = pygame.font.Font(self.font_path, self.font_size_h2)

        text_you_died = font_you_died.render("YOU DIED", True, CYAN)
        text_press_r = font_press_r.render("Press R to Restart", True, CYAN)

        # Центральные координаты текста оповещающем о смерти:
        text_width, text_height = font_you_died.size("YOU DIED")

        DEATH_TEXT_CENTER =  (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height*2) // 2
        # Прорисовка текста оповещающем о смерти.
        screen.blit(text_you_died, DEATH_TEXT_CENTER)

        # Центральные координаты текста с просьбой перезапуска:
        text_width, text_height = font_press_r.size("Press R to restart")

        PRESS_R_TEXT_CENTER =  (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT + text_height) // 2
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


if __name__ == '__main__':
    # Создание объекта игры и запуск основной функции:
    game = Game()
    input_thread = threading.Thread(target=game.event_listener)
    input_thread.start()
    game.main()
