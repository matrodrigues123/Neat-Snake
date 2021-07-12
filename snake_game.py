import pygame
import random
import neat
import numpy as np
import os
from math import atan
from pygame.locals import *

pygame.init()
WIN_X = 800
WIN_Y = 800
HIGH_SCORE = 0
STAT_FONT = pygame.font.SysFont('comicsans', 50)
screen = pygame.display.set_mode((WIN_X, WIN_Y))
pygame.display.set_caption('Snake')


class Snake:
    def __init__(self, block_size):
        self.direction = 'right'
        self.clock_wise = ['right', 'down', 'left', 'up']
        self.idx = self.clock_wise.index(self.direction)
        self.speed = block_size
        self.head = [200, 200]
        self.body = [self.head, [190, 200], [180, 200]]

    def move(self):
        if self.direction == 'right':
            self.head[0] += self.speed
        elif self.direction == 'left':
            self.head[0] -= self.speed
        elif self.direction == 'down':
            self.head[1] += self.speed
        elif self.direction == 'up':
            self.head[1] -= self.speed

    def straight(self):
        self.move()

    def right(self):
        new_idx = (self.idx + 1) % 4
        self.direction = self.clock_wise[new_idx]
        self.move()

    def left(self):
        new_idx = (self.idx - 1) % 4
        self.direction = self.clock_wise[new_idx]
        self.move()

    # def left(self):
    #     if self.direction != 'right':
    #         self.head[0] -= self.speed
    #         self.direction = 'left'
    #
    # def right(self):
    #     if self.direction != 'left':
    #         self.head[0] += self.speed
    #         self.direction = 'right'
    #
    # def up(self):
    #     if self.direction != 'down':
    #         self.head[1] -= self.speed
    #         self.direction = 'up'
    #
    # def down(self):
    #     if self.direction != 'up':
    #         self.head[1] += self.speed
    #         self.direction = 'down'

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
        self.x = random.randrange(0, 800, block_size)
        self.y = random.randrange(0, 800, block_size)


def draw_grid(block_size):
    # Set the size of the grid block
    for x in range(0, WIN_X, block_size):
        for y in range(0, WIN_Y, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


def get_data(snake, apple):
    if snake.head[1] != apple.y:
        angle = atan((snake.head[0] - apple.x) / (snake.head[1] - apple.y))
    else:
        angle = 0
    return (snake.head[0] - apple.x), (snake.head[1] - apple.y), angle


def main(genomes, config):
    nets = []
    ge = []
    snakes = []

    global HIGH_SCORE
    block_size = 40
    clock = pygame.time.Clock()
    apple_present = False

    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake(block_size))
        ge.append(g)

    while True:
        if not apple_present:
            apple = Apple(block_size)
            apple_present = True

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))
        draw_grid(block_size)

        # Draw the apple
        if apple_present:
            pygame.draw.rect(screen, (255, 0, 0), (apple.x, apple.y, block_size, block_size))
        # Loop through snakes
        for i, snake in enumerate(snakes):
            # Draw snake's body
            for square in snake.body:
                if square == snake.head:
                    pygame.draw.rect(screen, (0, 255, 0), (square[0], square[1], block_size, block_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 0), (square[0], square[1], block_size, block_size))

            # Eat apple
            if snake.head == [apple.x, apple.y]:
                ge[i].fitness += 5
                del apple
                apple = Apple(block_size)
            else:
                snake.body.pop(0)
            HIGH_SCORE = max(HIGH_SCORE, len(snake.body) - 3)

            # Collision
            if snake.collide():
                ge[i].fitness -= 10
                snakes.pop(i)
                nets.pop(i)
                ge.pop(i)

        # Give the outputs to the NN
        for i, snake in enumerate(snakes):
            output = nets[i].activate(get_data(snake, apple))
            if output[0] > 0.5:
                snake.straight()
            elif output[1] > 0.5:
                snake.right()
            elif output[2] > 0.5:
                snake.left()
            snake.body.append(list(snake.head))
        if len(snakes) == 0:
            break
        text = STAT_FONT.render(f'Highest Score:{HIGH_SCORE} ', 1, (255, 255, 0))
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(20)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
