import pygame
import random
import neat
import os
from math import atan
from pygame.locals import *
from plot_results import plot_stats, plot_species
from draw_net import draw_net

# pygame parameters
pygame.init()
WIN_X = 600
WIN_Y = 600
HIGH_SCORE = 0
STAT_FONT = pygame.font.SysFont('arial', 30)
screen = pygame.display.set_mode((WIN_X, WIN_Y))
pygame.display.set_caption('Snake')

# rgb colors
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
RED1 = (219, 75, 59)
RED2 = (252, 137, 121)
GREEN = (162, 232, 58)
BLACK = (0, 0, 0)


class Snake:
    def __init__(self, block_size):
        self.direction = 'right'
        self.clock_wise = ['right', 'down', 'left', 'up']
        self.move_count = 0
        self.speed = block_size
        self.head = [200, 200]
        self.body = [self.head, [190, 200], [180, 200]]

    def left(self):
        self.head[0] -= self.speed
        self.direction = 'left'

    def right(self):
        self.head[0] += self.speed
        self.direction = 'right'

    def up(self):
        self.head[1] -= self.speed
        self.direction = 'up'

    def down(self):
        self.head[1] += self.speed
        self.direction = 'down'

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
        self.x = random.randrange(0, WIN_X, block_size)
        self.y = random.randrange(0, WIN_Y, block_size)


def draw_grid(block_size):
    # Set the size of the grid block
    for x in range(0, WIN_X, block_size):
        for y in range(0, WIN_Y, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


def get_data(snake, apple, block_size):
    # Angle between snake head and apple
    if snake.head[1] != apple.y:
        angle = atan((snake.head[0] - apple.x) / (snake.head[1] - apple.y))
    else:
        angle = 0

    # Check if there is danger in direction [N, NE, E, SE, S, SW, W, NW]
    def check_danger(pos):
        if pos in snake.body or not 0 <= pos[0] <= WIN_X or not 0 <= pos[1] < WIN_Y:
            return True
        else:
            return False

    danger = [False, False, False, False, False, False, False, False]
    N = [snake.head[0], snake.head[1] - block_size]
    danger[0] = check_danger(N)

    NE = [snake.head[0] + block_size, snake.head[1] - block_size]
    danger[1] = check_danger(NE)

    E = [snake.head[0] + block_size, snake.head[1]]
    danger[2] = check_danger(E)

    SE = [snake.head[0] + block_size, snake.head[1] + block_size]
    danger[3] = check_danger(SE)

    S = [snake.head[0], snake.head[1] + block_size]
    danger[4] = check_danger(S)

    SW = [snake.head[0] - block_size, snake.head[1] + block_size]
    danger[5] = check_danger(SW)

    W = [snake.head[0] - block_size, snake.head[1]]
    danger[6] = check_danger(W)

    NW = [snake.head[0] - block_size, snake.head[1] - block_size]
    danger[7] = check_danger(NW)

    return (snake.head[0] - apple.x, snake.head[1] - apple.y, angle) + tuple(danger)


def main(genomes, config):
    nets = []
    ge = []
    snakes = []
    apples = []

    global HIGH_SCORE
    block_size = 40
    clock = pygame.time.Clock()

    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake(block_size))
        apples.append(Apple(block_size))
        ge.append(g)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        screen.fill(BLACK)
        # draw_grid(block_size)

        # Loop through snakes
        for i, snake in enumerate(snakes):
            # Draw snake's body
            for square in snake.body:
                if square == snake.head:
                    pygame.draw.rect(screen, BLUE1, (square[0], square[1], block_size, block_size))
                    pygame.draw.rect(screen, GREEN, (square[0] + 4, square[1] + 4, 30, 30))
                else:
                    pygame.draw.rect(screen, BLUE1, (square[0], square[1], block_size, block_size))
                    pygame.draw.rect(screen, BLUE2, (square[0] + 4, square[1] + 4, 30, 30))
            # Draw apple
            pygame.draw.rect(screen, RED1, (apples[i].x, apples[i].y, block_size, block_size))
            pygame.draw.rect(screen, RED2, (apples[i].x+4, apples[i].y+4, 30, 30))

            # Eat apple
            if snake.head == [apples[i].x, apples[i].y]:
                ge[i].fitness += 20
                snake.move_count = 0
                apples[i] = Apple(block_size)
            else:
                snake.body.pop(0)

            # Collision
            if snake.collide() or snake.move_count >= 120:
                ge[i].fitness -= (10 + snake.move_count//10)
                snakes.pop(i)
                nets.pop(i)
                ge.pop(i)
                apples.pop(i)

        # Give the outputs to the NN
        for i, snake in enumerate(snakes):
            output = nets[i].activate(get_data(snake, apples[i], block_size))
            if output[0] > 0.5 and snake.direction != 'right':
                snake.left()
            elif output[1] > 0.5 and snake.direction != 'left':
                snake.right()
            elif output[2] > 0.5 and snake.direction != 'down':
                snake.up()
            elif output[3] > 0.5 and snake.direction != 'up':
                snake.down()
            snake.body.append(list(snake.head))
            snake.move_count += 1
            HIGH_SCORE = max(HIGH_SCORE, len(snake.body) - 3)
        if len(snakes) == 0:
            break
        text = STAT_FONT.render(f'Best Score:{HIGH_SCORE} ', 1, (255, 255, 255))
        screen.blit(text, (10, 10))
        text = STAT_FONT.render(f'Alive:{len(snakes)} ', 1, (255, 255, 255))
        screen.blit(text, (10, 50))
        pygame.display.update()
        clock.tick(60)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 10)

    # draw_net(config, winner)
    plot_stats(stats, ylog=False, view=True)
    plot_species(stats, view=True)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
