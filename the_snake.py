"""Реализация игровых классов и игровой логики змейки."""
import os
from random import randint

import pygame as pg

from map import GameField


# Состояние игры.
running = True

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
YELLOW_COLOR_1 = (243, 250, 17)  # Цвет яблока 1
YELLOW_COLOR_2 = (211, 217, 15)  # Цвет яблока 2
YELLOW_COLOR_3 = (245, 250, 80)  # Цвет яблока 3
CYAN_COLOR_1 = (111, 235, 247)  # Цвет змеи 1
CYAN_COLOR_2 = (61, 159, 168)  # Цвет змеи 2
CYAN_COLOR_3 = (171, 248, 255)  # Цвет змеи 3
APPLE_COLORS = [YELLOW_COLOR_1, YELLOW_COLOR_2, YELLOW_COLOR_3]
SNAKE_COLORS = [CYAN_COLOR_1, CYAN_COLOR_2, CYAN_COLOR_3]

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100), 0, 32)
# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Класс, представляющий игровой объект.

    Атрибуты:
        position (list):
            координаты расположения игрового объекта

    Методы:
        draw(self, screen, body_color):
            Отрисовывает игровой объект на экране.

    """

    position = [0, 0]
    body_color = 0, 0, 0

    def __init__(self, position=[0, 0]):
        """Инициализирует базовые атрибуты игрового объекта."""
        self.position = position

    def draw(self, screen, body_color):
        """Отрисовывает игровой объект на экране."""
        cell = self.game_field[self.position[0]][self.position[1]]
        rect = pg.Rect(cell, (GRID_SIZE + 2, GRID_SIZE + 2))
        pg.draw.rect(screen, body_color, rect)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре.

    Этот класс отвечает за генерацию координат и
    отображение яблока на игровом поле.

    Атрибуты:
        game_field (list):
            Двумерный массив, представляющий игровое поле.

    Методы:
        __init__(snake_positions):
            Инициализирует объект яблока
            и устанавливает его начальное положение.

        randomize_position(snake_positions):
            Генерирует случайное положение яблока на игровом поле,
            исключая координаты змеи.
    """

    def __init__(self, snake_positions=[0, 0]):
        """Инициализирует объект и устанавливает начальное положение яблока.

        Args:
            snake_positions (list):
                Координаты змеи на игровом поле.

            game_field (GameField):
                Объект представляющий логические позиции
                поля игры.
        """
        self.randomize_position(snake_positions)
        self.game_field = GameField(FIELD_WIDTH, FIELD_HEIGHT).field

    def randomize_position(self, snake_positions):
        """Генерирует случайные координаты яблока на игровом поле.

        Args: snake_positions (list): Координаты змеи на игровом поле.
        """
        while True:
            apple_x = randint(0, FIELD_WIDTH - 1)
            apple_y = randint(0, FIELD_HEIGHT - 1)
            if [apple_x, apple_y] not in snake_positions:
                self.position = (apple_x, apple_y)
                break


class Snake(GameObject):
    """Класс, представляющий змею в игре.

    Этот класс обеспечивает логику и поведение змеи в игровом мире.

    Атрибуты:
        direction (tuple):
            Текущее направление движения змеи.

        next_direction (tuple):
            Следующее направление движения змеи.

        positions (list):
            Список координат сегментов змеи на игровом поле.

        game_field (list):
            Двумерный массив, представляющий игровое поле.

    Методы:
        draw_snake(self, screen, body_color):
            Отрисовывает тело змея.

        move(self):
            Обновлеяеет, удаляет координаты змеи в positions
            с учетом ее направления.

        get_next_head_position(self):
            Вычисление следующей позиции головы.

        get_head_position(self):
            Возращает текущую позицию головы змеи.

        get_tail_position(self):
            Возращает текущую позицию хвоста змеи.

        reset():
            Сбрасывает состояние змеи до начального.

    """

    def __init__(self):
        """Инициализирует объект и устанавливает положение змеи на поле.

        Args:
            snake (list): Начальное положение змеи на поле.
            field (list): Игровое поле, полезно для отрисовки змеи.
        """
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [[16, 10], [16, 11], [16, 12]]
        self.game_field = GameField(FIELD_WIDTH, FIELD_HEIGHT).field

    def draw_snake(self, screen, body_color):
        """Отрисовывает тело змея.

        Args:
            screen (display.surface):
                Экран игры.

            body_color (tuple):
                Цвет змеи.
        """
        self.body_color = body_color
        # Отрисовка змея
        for position in self.positions:
            self.position = [position[0], position[1]]
            super().draw(screen, self.body_color)

    def move(self):
        """Обновлеяеет, удаляет координаты змеи в positions."""
        # Добавление головы змеи в positions
        self.positions.insert(0, self.get_next_head_position())
        # Удаление хвоста змеи из positions
        self.positions.pop(-1)

    def get_next_head_position(self):
        """Вычисление следующей позиции головы."""
        x_head, y_head = self.get_head_position()

        # Если голова змеи достигла края,
        # переносим голову в противоположнную сторону
        if y_head == FIELD_HEIGHT - 1 and self.direction == DOWN:
            self.position = [x_head, 0]
        elif y_head == 0 and self.direction == UP:
            self.position = [x_head, FIELD_HEIGHT - 1]
        elif x_head == FIELD_WIDTH - 1 and self.direction == RIGHT:
            self.position = [0, y_head]
        elif x_head == 0 and self.direction == LEFT:
            self.position = [FIELD_WIDTH - 1, y_head]
        else:
            # Если змея не достигла края, просто обновляем ее позицию

            self.position[0] = x_head + self.direction[0]
            self.position[1] = y_head + self.direction[1]

        return self.position

    def update_direction(self, direction):
        """Обновляет направление."""
        self.direction = direction

    def get_head_position(self):
        """Возращает текущую позицию головы змеи."""
        return self.positions[0]

    def get_tail_position(self):
        """Возращает текущую позицию хвоста змеи."""
        return self.positions[-1]

    def reset(self):
        """Сбрасывает состояние змеи до начального."""
        self = self.__init__()


def main():
    """Основная функция игры."""
    global running
    font = os.path.join("fonts", "8bitOperatorPlus8-Regular.ttf")
    # Размеры шрифтов.
    fs_h1 = 72
    fs_h2 = 24

    score = 0
    # Счетчики анимации яблока.
    anim_time = 0
    anim_tic = 0
    # Инициализация PyGame:
    pg.init()

    # Создание объекта змейки:
    snake = Snake()
    field = GameField(FIELD_WIDTH, FIELD_HEIGHT)
    # Создание объекта яблока:
    apple = Apple(snake.positions)
    sound_eat = pg.mixer.Sound("sound/eat.mp3")
    sound_move = pg.mixer.Sound("sound/move.mp3")
    crash = False

    # Заголовок окна игрового поля:
    pg.display.set_caption('SNAKEEEE')

    while running:
        check_closing_event()
        # Управление частотой кадров:
        clock.tick(SPEED)
        # Проверка столкновения змейки с самой собой:
        if not crash:
            crash = check_crash(snake, score)

        if crash:
            score, crash = view_death(screen, font, fs_h1, fs_h2, score, snake)
        else:
            handle_keys(snake, sound_move)
            # Очистка экрана:
            screen.fill(BACKGROUND)
            # Отрисвока имени и рекорда
            view_name_and_score(font, fs_h2, score)
            # Двигаем змейку
            snake.move()

            # Отрисовка сетки:
            field.draw_grid(screen, CYAN_COLOR_1)
            # Изменения счетчиков анимации
            anim_tic, anim_time = animation_tic(anim_tic, anim_time)
            anim_tic += 1

            apple.draw(screen, APPLE_COLORS[anim_time])
            # Отрисовка змейки:
            snake.draw_snake(screen, SNAKE_COLORS[anim_time])

            if check_snake_collision(snake, apple.position):
                apple = Apple(snake.positions)
                score += 1
                sound_eat.play()
                screen.fill(CYAN_COLOR_1)

            # Обновление экрана:
            pg.display.update()

    # Завершение игры:
    pg.quit()


def animation_tic(anim_tic, anim_time):
    """сопровождает анимацию."""
    # Отрисовка яблока c анимацией:
    if anim_tic == 3:
        anim_time += 1
        anim_tic = 0

    if anim_time > 2:
        anim_time = 0

    return anim_tic, anim_time


def check_snake_collision(snake, apple_position):
    """Проверяет столкновение яблока и змейки."""
    if tuple(snake.positions[0]) == apple_position:
        snake.positions.append(snake.positions[-1] + list(snake.direction))
        snake.positions.append(snake.positions[-1] + list(snake.direction))
        return True
    return False


def check_closing_event():
    """Проверяет закрывающие событие."""
    global running
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False


def check_crash(snake, score):
    """Проверяет столкновение змейки с собой."""
    sound_crash = pg.mixer.Sound("sound/crash.mp3")

    for i in range(1, len(snake.positions)):
        if snake.positions[0] == snake.positions[i]:
            sound_crash.play()
            print(f"Score: {score}")
            return True


def view_death(screen, font, fs_h1, fs_h2, score, snake):
    """Функция для отображения экрана смерти."""
    global running
    sound_reload = pg.mixer.Sound("sound/reload.mp3")
    # Очищаем экран.
    screen.fill(BACKGROUND)
    # Уведомляем пользователя о его смерти.
    # Спрашиваем хочет ли он начать сначала.

    # Создание объектов текста
    font_you_died = pg.font.Font(font, fs_h1)
    font_press_r = pg.font.Font(font, fs_h2)

    str_h1 = "YOU DIED"
    str_h2 = "Press R to Restart"
    text_you_died = font_you_died.render(str_h1, True, CYAN_COLOR_1)
    text_press_r = font_press_r.render(str_h2, True, YELLOW_COLOR_3)

    # Центральные координаты текста оповещающем о смерти:
    text_width, text_height = font_you_died.size(str_h1)

    x = (SCREEN_WIDTH - text_width) // 2
    y = ((SCREEN_HEIGHT + 100) - text_height * 2) // 2
    death_text_center = x, y
    # Прорисовка текста оповещающем о смерти.
    screen.blit(text_you_died, death_text_center)

    # Центральные координаты текста с просьбой перезапуска:
    text_width, text_height = font_press_r.size(str_h2)

    x = (SCREEN_WIDTH - text_width) // 2
    y = ((SCREEN_HEIGHT + 100) + text_height) // 2
    press_r_text_center = x, y
    # Прорисовка текста оповещающем о смерти.
    screen.blit(text_press_r, press_r_text_center)
    # обновляем экран
    pg.display.update()

    # Прослушиваем событие нажатия кнопки R
    for event in pg.event.get():
        keys = pg.key.get_pressed()
        if event.type == pg.QUIT:
            running = False
        if keys[pg.K_r]:
            # Перезапускаем игру
            snake.reset()
            sound_reload.play()
            return 0, False

    return 0, True


def view_name_and_score(font, font_size, score):
    """Функция для отображения имени игрока и текущего счета."""
    nickname = "bulatue"
    # Создание объектов текста
    font_score = pg.font.Font(font, font_size)
    font_nickname = pg.font.Font(font, font_size)

    text_score = font_score.render(str(score), True, YELLOW_COLOR_3)
    text_nickname = font_nickname.render(nickname, True, CYAN_COLOR_1)

    text_score_size = SCREEN_WIDTH - 60, SCREEN_HEIGHT + 40
    # Прорисовка рекорда.
    screen.blit(text_score, text_score_size)

    text_score_nickname = 30, SCREEN_HEIGHT + 40
    # Прорисовка моего имени.
    screen.blit(text_nickname, text_score_nickname)


def handle_keys(snake, sound_move):
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
            snake.update_direction(direction)
            sound_move.play()
            return None


def opposite_direction(direction):
    """Возвращает противоположное направление."""
    return {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,
    }[direction]


if __name__ == '__main__':
    try:
        main()
    except Exception as _:
        print("Snake is not alive")
