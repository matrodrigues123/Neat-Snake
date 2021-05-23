import pygame
import random
import neat
import os
from math import atan
from pygame.locals import *

pygame.init()
WIN_X = 800
WIN_Y = 800
STAT_FONT = pygame.font.SysFont('comicsans', 50)
screen = pygame.display.set_mode((WIN_X, WIN_Y))
pygame.display.set_caption('Snake')


class Snake:
    def __init__(self, block_size):
        self.direction = 'right'
        self.speed = block_size
        self.head = [200, 200]
        self.body = [self.head, [190, 200], [180, 200]]

    def left(self):
        if self.direction != 'right':
            self.head[0] -= self.speed

    def right(self):
        if self.direction != 'left':
            self.head[0] += self.speed

    def up(self):
        if self.direction != 'down':
            self.head[1] -= self.speed

    def down(self):
        if self.direction != 'up':
            self.head[1] += self.speed

    def collide(self):
        colision_count = 0
        for square in self.body:
            if square == self.head:
                colision_count += 1
            if colision_count > 1:
                return True
        if not 0 <= self.head[0] <= WIN_X or not 0 <= self.head[1] < WIN_Y:
            return True
        else:
            return False


class Apple:
    def __init__(self, block_size):
        self.x = random.randrange(0, 600, block_size)
        self.y = random.randrange(0, 600, block_size)


def draw_grid(block_size):
    # Set the size of the grid block
    for x in range(0, WIN_X, block_size):
        for y in range(0, WIN_Y, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


def main():
    block_size = 40
    clock = pygame.time.Clock()
    snake = Snake(block_size)
    apple_present = False

    while True:
        if not apple_present:
            apple = Apple(block_size)
            apple_present = True

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            # Controls (not needed when AI is implemented)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != 'right':
                    snake.direction = 'left'
                if event.key == pygame.K_RIGHT and snake.direction != 'left':
                    snake.direction = 'right'
                if event.key == pygame.K_UP and snake.direction != 'down':
                    snake.direction = 'up'
                if event.key == pygame.K_DOWN and snake.direction != 'up':
                    snake.direction = 'down'

        screen.fill((0, 0, 0))
        draw_grid(block_size)

        # Draw the apple
        if apple_present:
            pygame.draw.rect(screen, (255, 0, 0), (apple.x, apple.y, block_size, block_size))

        # Detect collision
        if snake.collide():
            pygame.quit()
            exit()

        # Draw snake's body
        for square in snake.body:
            if square == snake.head:
                pygame.draw.rect(screen, (0, 255, 0), (square[0], square[1], block_size, block_size))
            else:
                pygame.draw.rect(screen, (255, 255, 0), (square[0], square[1], block_size, block_size))

        # Movement(not needed when AI is implemented)
        if snake.direction == 'left':
            snake.left()
        elif snake.direction == 'right':
            snake.right()
        elif snake.direction == 'up':
            snake.up()
        elif snake.direction == 'down':
            snake.down()
        snake.body.append(list(snake.head))
        # Eat apple
        if snake.head == [apple.x, apple.y]:
            apple_present = False
            del apple
        else:
            snake.body.pop(0)

        text = STAT_FONT.render('Score: ' + str(len(snake.body) - 3), 1, (255, 255, 0))
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(20)

main()