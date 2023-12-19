import pygame
import random
from enum import Enum
from abc import ABC, abstractmethod

# Создание перечисления для направлений движения змейки
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# Интерфейс для класса наблюдателя
class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

# Класс змейки
class Snake(Observer):
    def __init__(self):
        self.body = [(100, 50), (90, 50), (80, 50)]  # Начальное положение змейки
        self.direction = Direction.RIGHT
        self.grow = False
        self.score = 0
        self.game_over = False

    def update(self):
        self.move()
        self.check_collision()
        self.check_out_of_bounds()

    def move(self):
        head = self.body[0]
        x, y = head

        if self.direction == Direction.UP:
            new_head = (x, y - 10)
        elif self.direction == Direction.DOWN:
            new_head = (x, y + 10)
        elif self.direction == Direction.LEFT:
            new_head = (x - 10, y)
        elif self.direction == Direction.RIGHT:
            new_head = (x + 10, y)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        if new_direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = new_direction
        elif new_direction == Direction.DOWN and self.direction != Direction.UP:
            self.direction = new_direction
        elif new_direction == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = new_direction
        elif new_direction == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head == segment:
                self.game_over = True

    def check_out_of_bounds(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= 600 or head[1] < 0 or head[1] >= 400:
            self.game_over = True

    def increase_length(self):
        self.grow = True
        self.score += 1

    def get_head_position(self):
        return self.body[0]

    def get_body(self):
        return self.body

    def get_score(self):
        return self.score

    def is_game_over(self):
        return self.game_over

# Класс еды
class Food(Observer):  # Добавлено наследование от Observer
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, 59) * 10, random.randint(0, 39) * 10)

    def get_position(self):
        return self.position

    def update(self):
        pass  # Пустой метод update, так как еда не изменяется во времени игры


# Фабричный метод для создания объектов змейки и еды
class GameObjectFactory(ABC):
    @abstractmethod
    def create_snake(self):
        pass

    @abstractmethod
    def create_food(self):
        pass

# Конкретная реализация фабричного метода
class ConcreteGameObjectFactory(GameObjectFactory):
    def create_snake(self):
        return Snake()

    def create_food(self):
        return Food()

# Компоновщик для объединения игровых объектов
class CompositeGameObject:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def update(self):
        for obj in self.objects:
            obj.update()

# Класс игры
class Game:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.factory = ConcreteGameObjectFactory()
        self.game_objects = CompositeGameObject()
        self.snake = self.factory.create_snake()
        self.food = self.factory.create_food()
        self.game_objects.add_object(self.snake)
        self.game_objects.add_object(self.food)
        self.spawn_food()

    def spawn_food(self):
        self.food.randomize_position()
        # Проверка, чтобы новая еда не появилась на теле змейки
        while self.food.get_position() in self.snake.get_body():
            self.food.randomize_position()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(Direction.RIGHT)

            self.screen.fill((0, 0, 0))

            self.game_objects.update()

            # Отображение змейки
            for segment in self.snake.get_body():
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))

            # Отображение еды
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food.get_position()[0], self.food.get_position()[1], 10, 10))

            # Проверка на столкновение змейки с едой
            if self.snake.get_head_position() == self.food.get_position():
                self.snake.increase_length()
                self.spawn_food()

            # Проверка на окончание игры
            if self.snake.is_game_over():
                running = False

            pygame.display.update()
            self.clock.tick(10)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
