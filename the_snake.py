import threading
import pygame
import os
from random import randint

from map import GameField
# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 642, 482
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
CYAN = (111, 235, 247)  # Цвет границы ячейки
YELLOW_COLOR_1 = (243, 250, 17)  # Цвет яблока 1
YELLOW_COLOR_2 = (211, 217, 15)  # Цвет яблока 2
YELLOW_COLOR_3 = (245, 250, 80)  # Цвет яблока 3
SNAKE_COLOR = (111, 235, 247)  # Цвет змейки
APPLE_COLOR = (255, 0, 0)

# Скорость движения змейки:
SPEED = 15


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('SNAKEEEE')
# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Класс, представляющий игровой объект."""

    position = (0, 0)
    body_color = None

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

    body_color = APPLE_COLOR

    def __init__(self, snake_positions=(0, 0), field=None):
        """Инициализирует объект и устанавливает начальное положение яблока.

        Args:
            snake_positions (list): Координаты змеи на игровом поле.
            Field (object): Объект поля игры.
        """
        self.position = self.randomize_position(snake_positions)
        self.game_field = field
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
    double_direction = False
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self, snake=(0, 0), field=[0, 0]):
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
        # Обработка события, если змейка достигла края окна
        x_head, y_head = self.get_head_position()
        end_field = True

        if y_head == FIELD_HEIGHT - 1 and self.direction == DOWN:
            y_head = 0
        elif y_head == 0 and self.direction == UP:
            y_head = FIELD_HEIGHT - 1
        elif x_head == FIELD_WIDTH - 1 and self.direction == RIGHT:
            x_head = 0
        elif x_head == 0 and self.direction == LEFT:
            x_head = FIELD_WIDTH - 1
        else:
            end_field = False

        if not end_field:
            x_next = x_head + self.direction[0]
            y_next = y_head + self.direction[1]
        else:
            x_next, y_next = x_head, y_head

        self.positions.insert(0, [x_next, y_next])

        # Рисуем голову змеи
        snake_head = self.game_field[x_next][y_next]
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
    animation_timer = 0

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
        self.apple = Apple(self.snake.positions, self.field.field)

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
                    self.apple = Apple(self.snake.positions, self.field.field)
                    screen.fill(CYAN)
                    self.score += 1

                # Отрисовка сетки:
                self.field.draw_grid(screen)
                # Отрисовка яблока c анимацией:
                if self.animation_timer == 3:
                    self.apple_animation_tic += 1
                    self.animation_timer = 0

                if self.apple_animation_tic > 2:
                    self.apple_animation_tic = 0

                self.apple.draw(screen, self.apple_animation_tic)
                self.animation_timer += 1

                # Обновление экрана:
                pygame.display.update()

        # Завершение игры:
        pygame.quit()

    def view_death_screen(self):
        """Функция для отображения экрана смерти."""
        # Отчищаем экран.
        print(f"Score: {self.score}")
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
                self.snake.direction = UP
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
        handle_double_keys(game, keys)
        handle_single_keys(game, keys)
        game.snake.update_direction()


def handle_double_keys(game, keys):
    """Обработка двойных нажатий клавиш."""
    double_key_actions = {
        (pygame.K_RIGHT, pygame.K_DOWN): (RIGHT, DOWN),
        (pygame.K_LEFT, pygame.K_DOWN): (LEFT, DOWN),
        (pygame.K_LEFT, pygame.K_UP): (LEFT, UP),
        (pygame.K_RIGHT, pygame.K_UP): (RIGHT, UP),
        (pygame.K_UP, pygame.K_LEFT): (UP, LEFT),
        (pygame.K_DOWN, pygame.K_LEFT): (DOWN, LEFT),
        (pygame.K_UP, pygame.K_RIGHT): (UP, RIGHT),
        (pygame.K_DOWN, pygame.K_RIGHT): (DOWN, RIGHT),
    }
    for keys_combination, directions in double_key_actions.items():
        if keys[keys_combination[0]] and keys[keys_combination[1]]:
            game.snake.direction = directions[0]
            game.snake.next_direction = directions[1]


def handle_single_keys(game, keys):
    """Обработка одиночных нажатий клавиш."""
    key_actions = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }
    for key, direction in key_actions.items():
        if keys[key] and game.snake.direction != opposite_direction(direction):
            game.snake.next_direction = direction


def opposite_direction(direction):
    """Возвращает противоположное направление."""
    return {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,
    }[direction]


def main():
    """Запуск потоков игры."""
    # Создание объекта игры и запуск основной функции:
    game = Game()
    input_thread = threading.Thread(target=handle_keys, args=(game,))
    input_thread.start()
    game.main()


if __name__ == '__main__':
    main()
