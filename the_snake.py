from random import choice, randint

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self,
                 body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR,
                 position: tuple[int, int] = SCREEN_CENTER) -> None:
        self.position: tuple[int, int] = position
        self.body_color: tuple[int, int, int] = body_color

    def draw(self) -> None:
        """Отрисовывает объект на поле, переопределяется в наследниках."""
        pass

    def draw_cell(self,
                  position: tuple[int, int],
                  body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR,
                  border_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
                  ) -> None:
        """Рисует одну клетку на игровом поле."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Яблоко - пища для змейки."""

    def __init__(self) -> None:
        super().__init__(APPLE_COLOR, Apple.randomize_position())

    def draw(self) -> None:
        """Рисует яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color)

    @staticmethod
    def randomize_position() -> tuple[int, int]:
        """Рассчитывает случайные координаты внутри игрового поля."""
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return position_x, position_y


class Snake(GameObject):
    """Змейка - перемещается по полю и поедает яблоки."""

    def __init__(self) -> None:
        super().__init__(SNAKE_COLOR)
        self.length: int = 1
        self.positions: list[tuple[int, int]] = [(SCREEN_CENTER)]
        self.direction: tuple[int, int] = RIGHT
        self.next_direction: tuple[int, int] | None = None
        self.last: tuple[int, int] | None = None

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Движение змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            ((head_x + GRID_SIZE * dx + GRID_WIDTH) % GRID_WIDTH),
            ((head_y + GRID_SIZE * dy + GRID_HEIGHT) % GRID_HEIGHT)
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def update_direction(self) -> None:
        """Обновляет направление после нажатия не кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Рисует все клетки змейки и стирает хвост."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)
        if self.last:
            self.draw_cell(self.last)
            self.last = None


def main():
    """Описывает логику игры и игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    ...

    # while True:
    #     clock.tick(SPEED)

    # Тут опишите основную логику игры.
    # ...


if __name__ == '__main__':
    main()


# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT
