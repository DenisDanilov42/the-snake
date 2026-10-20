from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
HALF_WIDTH = SCREEN_WIDTH // 2 - GRID_SIZE
HALF_HEIGHT = SCREEN_HEIGHT // 2 - GRID_SIZE

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

# Словарь поворотов Змейки
turns = {(pygame.K_UP, UP): UP,
         (pygame.K_UP, LEFT): UP,
         (pygame.K_UP, RIGHT): UP,
         (pygame.K_DOWN, DOWN): DOWN,
         (pygame.K_DOWN, RIGHT): DOWN,
         (pygame.K_DOWN, LEFT): DOWN,
         (pygame.K_LEFT, UP): LEFT,
         (pygame.K_LEFT, DOWN): LEFT,
         (pygame.K_LEFT, LEFT): LEFT,
         (pygame.K_RIGHT, UP): RIGHT,
         (pygame.K_RIGHT, DOWN): RIGHT,
         (pygame.K_RIGHT, RIGHT): RIGHT}


class GameObject:
    """Родительский объект."""

    flag_reset = False
    ocuppied_positions: list[tuple] = []

    def __init__(self, body_color=BORDER_COLOR) -> None:
        self.position = (HALF_WIDTH, HALF_HEIGHT)
        self.body_color = body_color

    def draw(self) -> None:
        """Обеспечивает инициализацию базового метода отображения объектов."""


class Apple(GameObject):
    """Объект Яблоко.
    При поедании его длина и скорость Змейки увеличиваются.
    """

    def __init__(self, body_color=APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.randomize_position()

    # зачем каждый раз передавать параметр с занятыми ячейками на поле,
    # при вызове метода, если он реализован как атрибут
    # родительского класса ocuppied_positions или я не понимаю идею,
    # тогда мне нужен контакт для общения

    def randomize_position(
            self,
            occupied_position=(HALF_WIDTH, HALF_HEIGHT)) -> None:
        """Обеспечивает случайное расположение объектов на поле без повторов,
        наполнение и очищение списка занятых позиций
        """
        if occupied_position in self.ocuppied_positions:
            self.ocuppied_positions.remove(occupied_position)
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if (position != occupied_position
               and position not in self.ocuppied_positions):
                self.position = position
                self.ocuppied_positions.append(position)
                break

    def draw(self) -> None:
        """Обеспечивает отображение объекта на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self) -> None:
        """Сбрасывает настройки для начала новой игры."""
        self.randomize_position()


class BadApple(Apple):
    """Объект Испорченное яблоко.
    При поедании его длина Змейки уменьшается, а скорость увеличивается.
    """

    def __init__(self, body_color=BAD_APPLE_COLOR):
        super().__init__(body_color)


class Stone(Apple):
    """Объект Камень.
    При столкновении с ним Змейки игра начинается сначала.
    """

    def __init__(self, body_color=STONE_COLOR):
        super().__init__(body_color)


class Snake(GameObject):
    """Объект Змейка. Осуществляет работу Змейки."""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self) -> tuple:
        """Возвращает головной кортеж Змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Обеспечивает расчет движения Змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * GRID_SIZE, head_y + dir_y * GRID_SIZE)
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
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, next_direction) -> None:
        """Обеспечивает обновление направления после нажатия на кнопку."""
        self.direction = next_direction

    def check_border(self) -> None:
        """Обеспечивает прохождение сквозь границы поля."""
        head_х, head_y = self.get_head_position()
        if head_х % SCREEN_WIDTH == 0:
            self.positions[0] = (0, head_y)
        if head_х == -GRID_SIZE:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE, head_y)
        if head_y % SCREEN_HEIGHT == 0:
            self.positions[0] = (head_х, 0)
        if head_y == -GRID_SIZE:
            self.positions[0] = (head_х, SCREEN_HEIGHT - GRID_SIZE)

    def reset(self) -> None:
        """Сбрасывает настройки для начала новой игры."""
        self.lenght = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.speed = SPEED


def handle_keys(game_object) -> None:
    """Обеспечивает управление Змейкой с помощью клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            key_direction = (event.key, game_object.direction)
            if key_direction in turns:
                game_object.update_direction(turns[key_direction])


def check_eat_apple(snake_object, apple_object) -> None:
    """Обеспечивает увеличение длины Змейки после съедания яблока."""
    if snake_object.get_head_position() == apple_object.position:
        snake_object.lenght += 1
        snake_object.speed += 1
        apple_object.randomize_position(apple_object.position)


def check_eat_bad_apple(snake_object, bad_apple_object) -> None:
    """Обеспечивает уменьшение длины Змейки после съедания
    испорченного яблока.
    """
    if snake_object.get_head_position() == bad_apple_object.position:
        if snake_object.lenght > 1:
            del snake_object.positions[0]
            snake_object.lenght -= 1
            snake_object.speed += 1
            bad_apple_object.randomize_position(bad_apple_object.position)
        else:
            snake_object.flag_reset = True


def check_eat_stone_itself(snake_object, stone_object) -> None:
    """Начинает новую игру после столкновения с камнем, или собой."""
    if (snake_object.get_head_position() == stone_object.position
       or snake_object.get_head_position() in snake_object.positions[1:]):
        snake_object.flag_reset = True


def reset_all_objects(snake_object, apple_object,
                      bad_apple_object, stone_object) -> None:
    """Сбрасывает все настройки объектов для начала новой игры."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple_object.ocuppied_positions.clear()
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
    while True:
        apple.draw()
        bad_apple.draw()
        stone.draw()
        handle_keys(snake)
        snake.move()
        snake.check_border()
        check_eat_apple(snake, apple)
        check_eat_bad_apple(snake, bad_apple)
        check_eat_stone_itself(snake, stone)
        if snake.flag_reset:
            reset_all_objects(snake, apple, bad_apple, stone)
        snake.draw()
        pygame.display.update()
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()[0]
