import pygame
import random
from pygame.locals import *

pygame.init()
WIN_X = 600
WIN_Y = 600
STAT_FONT = pygame.font.SysFont('comicsans', 50)
screen = pygame.display.set_mode((WIN_X, WIN_Y))
pygame.display.set_caption('Snake')


class Snake:
    def __init__(self):
        self.speed = 10
        self.head = [200, 200]
        self.body = [self.head, [190, 200], [180, 200]]

    def left(self):
        self.head[0] -= self.speed

    def right(self):
        self.head[0] += self.speed

    def up(self):
        self.head[1] -= self.speed

    def down(self):
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
    def __init__(self):
        self.x = random.randrange(0, 600, 10)
        self.y = random.randrange(0, 600, 10)


def main():
    clock = pygame.time.Clock()
    snake = Snake()
    direction = 'right'
    apple_present = False

    while True:
        if not apple_present:
            apple = Apple()
            apple_present = True

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

        # Draw the apple
        if apple_present:
            pygame.draw.rect(screen, (255, 0, 0), (apple.x, apple.y, 10, 10))

        # Detect collision
        if snake.collide():
            pygame.quit()
            exit()

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
        # Eat apple
        if snake.head == [apple.x, apple.y]:
            apple_present = False
            del apple
        else:
            snake.body.pop(0)

        text = STAT_FONT.render('Score: ' + str(len(snake.body) - 3), 1, (255, 255, 255))
        screen.blit(text, (WIN_X - 10 - text.get_width(), 10))

        pygame.display.update()
        clock.tick(25)

main()