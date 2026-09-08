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

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

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

    def __init__(self,
                 snake_positions: list[tuple[int, int]] | None = None
                 ) -> None:
        super().__init__(APPLE_COLOR)
        self.randomize_position(snake_positions)

    def draw(self) -> None:
        """Рисует яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)

    def randomize_position(self,
                           snake_positions: list[tuple[int, int]] | None
                           ) -> None:
        """Ставит яблоко в случайную точку поля."""
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (not snake_positions
                    or (position_x, position_y) not in snake_positions):
                self.position = position_x, position_y
                break


class Snake(GameObject):
    """Змейка - перемещается по полю и поедает яблоки."""

    def __init__(self) -> None:
        super().__init__(SNAKE_COLOR)
        self.length: int = 1
        self.positions: list[tuple[int, int]] = [SCREEN_CENTER]
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

    def reset(self) -> None:
        """Сбрасывает змейку к изначальному состоянию."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.last = None
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None


def handle_keys(snake: Snake) -> None:
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Создает игровые объекты и запускает игровой цикл."""
    pygame.init()

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
        pygame.display.update()


if __name__ == '__main__':
    main()
