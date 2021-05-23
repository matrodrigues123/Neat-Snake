import pygame
import random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')


class Snake:
    def __init__(self):
        self.speed = 10
        self.head = [200, 200]
        self.body = [[180, 200], [190, 200], self.head]

    def left(self):
        self.head[0] -= self.speed

    def right(self):
        self.head[0] += self.speed

    def up(self):
        self.head[1] -= self.speed

    def down(self):
        self.head[1] += self.speed

class Apple:
    def __init__(self):



def main():
    clock = pygame.time.Clock()
    snake = Snake()
    direction = 'right'
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            # Controls (not needed when AI is implemented)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                if event.key == pygame.K_RIGHT:
                    direction = 'right'
                if event.key == pygame.K_UP:
                    direction = 'up'
                if event.key == pygame.K_DOWN:
                    direction = 'down'

        screen.fill((0, 0, 0))

        # Draw snake's body
        for square in snake.body:
            pygame.draw.rect(screen, (255, 255, 255), (square[0], square[1], 10, 10))

        # Movement
        if direction == 'left':
            snake.left()
        elif direction == 'right':
            snake.right()
        elif direction == 'up':
            snake.up()
        elif direction == 'down':
            snake.down()
        snake.body.append(list(snake.head))
        snake.body.pop(0)

        pygame.display.update()
        clock.tick(30)

main()