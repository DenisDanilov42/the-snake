from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (0, 255, 0)

# Цвет испорченного яблока
BAD_APPLE_COLOR = (255, 255, 0)

# Цвет камня
STONE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 0, 255)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс игровых объектов."""

    # флаг общего сброса и начала новой игры
    flag_reset = False

    def __init__(self, body_color=BORDER_COLOR) -> None:
        # инициализация позиции в центре поля
        self.position = (SCREEN_WIDTH // 2 - GRID_SIZE,
                         SCREEN_HEIGHT // 2 - GRID_SIZE)
        self.body_color = body_color

    def draw(self) -> None:
        """Обеспечивает инициализацию базового метода отображения объектов."""
        pass


class Apple(GameObject):
    """Класс объекта Apple.
    При поедании его длина и скорость Змейки увеличиваются на 1.
    """

    def __init__(self, body_color=APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Обеспечивает случайное расположение объекта на поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        """Обеспечивает отображение объекта на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self) -> None:
        """Сбрасывает настройки для начала новой игры."""
        self.randomize_position()


class BadApple(Apple):
    """Класс объекта BadApple.
    При поедании его длина Змейки уменьшается, а скорость увеличивается на 1.
    """

    def __init__(self, body_color=BAD_APPLE_COLOR):
        super().__init__(body_color)


class Stone(Apple):
    """Класс объекта Stone.
    При столкновении с ним игра начинается сначала.
    """

    def __init__(self, body_color=STONE_COLOR):
        super().__init__(body_color)


class Snake(GameObject):
    """Класс объекта Snake.
    Обеспечивает работу Змейки.
    """

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.lenght = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.speed = SPEED

    def get_head_position(self) -> tuple:
        """Возвращает головной кортеж Змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Обеспечивает расчет движения Змейки."""
        current_head = self.get_head_position()
        new_head = (current_head[0] + self.direction[0] * GRID_SIZE,
                    current_head[1] + self.direction[1] * GRID_SIZE)
        list.insert(self.positions, 0, new_head)
        self.last = self.positions[-1]
        if len(self.positions) > self.lenght:
            del self.positions[-1]

    def draw(self) -> None:
        """Обеспечивает отображение движения Змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self) -> None:
        """Обеспечивает обновление направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def check_border(self) -> None:
        """Обеспечевает прохождение сквозь границы поля."""
        head = list(self.get_head_position())
        if head[0] % SCREEN_WIDTH == 0:
            self.positions[0] = (0, head[1])
        if head[0] == -GRID_SIZE:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE, head[1])
        if head[1] % SCREEN_HEIGHT == 0:
            self.positions[0] = (head[0], 0)
        if head[1] == -GRID_SIZE:
            self.positions[0] = (head[0], SCREEN_HEIGHT - GRID_SIZE)

    def reset(self) -> None:
        """Сбрасывает настройки для начала новой игры."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.lenght = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.speed = SPEED

    def check_eat_itself(self) -> None:
        """Начинает новую игру, если Змейка кусает себя."""
        if self.positions.count(self.get_head_position()) > 1:
            self.flag_reset = True


def handle_keys(game_object) -> None:
    """Обеспечевает управление Змейкой с помощью клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            game_object.update_direction()


def check_eat_apple(snake_object, apple_object) -> None:
    """Обеспечевает увеличение длины Змейки после съедания объекта Apple."""
    if snake_object.get_head_position() == apple_object.position:
        snake_object.lenght += 1
        snake_object.speed += 1
        apple_object.randomize_position()


def check_eat_bad_apple(snake_object, bad_apple_object) -> None:
    """Обеспечевает уменьшение длины Змейки после съедания объекта BadApple."""
    if snake_object.get_head_position() == bad_apple_object.position:
        if snake_object.lenght > 1:
            del snake_object.positions[0]
            snake_object.lenght -= 1
            snake_object.speed += 1
            bad_apple_object.randomize_position()
        else:
            snake_object.flag_reset = True


def check_eat_stone(snake_object, stone_object) -> None:
    """Начинает новую игру после столкновения с объектом Stone."""
    if snake_object.get_head_position() == stone_object.position:
        snake_object.flag_reset = True


def reset_all_objects(snake_object, apple_object,
                      bad_apple_object, stone_object) -> None:
    """Сбрасывает все настройки объектов для начала новой игры."""
    snake_object.reset()
    apple_object.reset()
    bad_apple_object.reset()
    stone_object.reset()
    snake_object.flag_reset = False


def main() -> None:
    """Обеспечевает основную логику игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    bad_apple = BadApple()
    stone = Stone()
    running = True
    while running:
        apple.draw()
        bad_apple.draw()
        stone.draw()
        handle_keys(snake)
        snake.move()
        snake.check_border()
        snake.check_eat_itself()
        check_eat_apple(snake, apple)
        check_eat_bad_apple(snake, bad_apple)
        check_eat_stone(snake, stone)
        snake.draw()
        if snake.flag_reset:
            reset_all_objects(snake, apple, bad_apple, stone)
        pygame.display.update()
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()[0]
