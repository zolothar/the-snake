"""Игра «Змейка».

Игрок управляет змейкой, которая движется по игровому полю.
Цель - увеличивать длину змейки, съедая появляющиеся на экране яблоки.

Архитектура скрипта the_snake.py:
* инициализация pygame;
* создание объектов (Snake, Apple);
* основной игровой цикл:
    - обработка событий;
    - обновление состояния игры;
    - проверка столкновений;
    - отрисовка объектов на экране.
"""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self,
                 body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR,
                 position: tuple[int, int] = SCREEN_CENTER) -> None:
        """Инициализирует объект базового класса цветом и координатами."""
        self.position: tuple[int, int] = position
        self.body_color: tuple[int, int, int] = body_color

    def draw(self) -> None:
        """Отрисовывает объект на поле, переопределяется в наследниках."""
        raise NotImplementedError(
            f'Переопределите draw() в {self.__class__.__name__}')

    def draw_cell(self,
                  position: tuple[int, int],
                  body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR,
                  border_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
                  ) -> None:
        """Рисует одну клетку на игровом поле."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Яблоко - пища для змейки."""

    def __init__(self,
                 forbidden_positions: list[tuple[int, int]] | None = None,
                 color: tuple[int, int, int] = APPLE_COLOR
                 ) -> None:
        """Инициализирует яблоко, положение выбирается в случайной
        свободной клетке.
        """
        super().__init__(color)
        self.randomize_position(forbidden_positions)

    def draw(self) -> None:
        """Рисует яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)

    def randomize_position(self,
                           forbidden_positions: list[tuple[int, int]] | None
                           ) -> None:
        """Ставит яблоко в случайную точку поля."""
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (not forbidden_positions
                    or (position_x, position_y) not in forbidden_positions):
                self.position = position_x, position_y
                break


class Snake(GameObject):
    """Змейка - перемещается по полю и поедает яблоки."""

    def __init__(self, color: tuple[int, int, int] = SNAKE_COLOR) -> None:
        """Инициализирует змейку."""
        super().__init__(color)
        self.reset()
        self.direction: tuple[int, int] = RIGHT

    def reset(self) -> None:
        """Сбрасывает змейку к изначальному состоянию."""
        self.length: int = 1
        self.positions: list[tuple[int, int]] = [SCREEN_CENTER]
        self.last: tuple[int, int] | None = None
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction: tuple[int, int] | None = None

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Движение змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            ((head_x + GRID_SIZE * dx + SCREEN_WIDTH) % SCREEN_WIDTH),
            ((head_y + GRID_SIZE * dy + SCREEN_HEIGHT) % SCREEN_HEIGHT)
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def update_direction(self) -> None:
        """Обновляет направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Рисует голову змейки и стирает хвост."""
        self.draw_cell(self.get_head_position(), self.body_color, BORDER_COLOR)
        if self.last:
            self.draw_cell(self.last)
            self.last = None


def handle_keys(snake: Snake) -> None:
    """Обработка нажатий клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit('Нажата кнопка выхода, игра завершена.')
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Создает игровые объекты и запускает игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
