#!/usr/bin/env python3
"""
Игра "Змейка" на Python с использованием Pygame
Управление: стрелки или WASD
"""

import pygame
import random
import sys
from enum import Enum

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# FPS
FPS = 10


class Direction(Enum):
    """Направления движения змейки"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """Класс змейки"""

    def __init__(self):
        """Инициализация змейки"""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.color = GREEN
        self.head_color = DARK_GREEN

    def get_head_position(self):
        """Получить позицию головы"""
        return self.positions[0]

    def update(self):
        """Обновить позицию змейки"""
        cur = self.get_head_position()
        x, y = self.direction.value
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)

        # Проверка столкновения с собой
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def reset(self):
        """Сброс змейки"""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT

    def render(self, surface):
        """Отрисовка змейки"""
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                             GRID_SIZE, GRID_SIZE)
            # Голова змейки темнее
            color = self.head_color if i == 0 else self.color
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

    def handle_keys(self):
        """Обработка нажатий клавиш"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # Стрелки
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                # WASD
                elif event.key == pygame.K_w and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_s and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_a and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_d and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True


class Food:
    """Класс еды"""

    def __init__(self):
        """Инициализация еды"""
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        """Случайная позиция еды"""
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        """Отрисовка еды"""
        rect = pygame.Rect(self.position[0] * GRID_SIZE,
                          self.position[1] * GRID_SIZE,
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Game:
    """Главный класс игры"""

    def __init__(self):
        """Инициализация игры"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Змейка')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True
        self.game_over = False

    def handle_events(self):
        """Обработка событий"""
        if not self.snake.handle_keys():
            self.running = False

        # Проверка на нажатие R для перезапуска
        if self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    def reset_game(self):
        """Сброс игры"""
        self.snake.reset()
        self.food.randomize_position()
        self.score = 0
        self.game_over = False

    def update(self):
        """Обновление игры"""
        if self.game_over:
            return

        # Обновление змейки
        if not self.snake.update():
            self.game_over = True
            return

        # Проверка поедания еды
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.score += 10
            self.food.randomize_position()

            # Проверка, что еда не на змейке
            while self.food.position in self.snake.positions:
                self.food.randomize_position()

    def render(self):
        """Отрисовка"""
        self.screen.fill(BLACK)

        # Отрисовка змейки и еды
        self.snake.render(self.screen)
        self.food.render(self.screen)

        # Отрисовка счета
        score_text = self.small_font.render(f'Счет: {self.score}', True, WHITE)
        self.screen.blit(score_text, (5, 5))

        # Отрисовка Game Over
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, RED)
            restart_text = self.small_font.render('Нажмите R для перезапуска', True, WHITE)
            quit_text = self.small_font.render('или ESC для выхода', True, WHITE)

            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))

            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(quit_text, quit_rect)

        pygame.display.update()

    def run(self):
        """Главный цикл игры"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Точка входа в программу"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
