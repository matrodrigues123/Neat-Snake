import pygame
import random
import neat
import time
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


def eval_genomes(genomes, config):
    nets= []
    ge=[]
    snakes=[]
    block_size = 40
    clock = pygame.time.Clock()
    # snakes = Snake(block_size)
    apple_present = False


    for _,g in genomes:
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        snakes.append(Snake(block_size))
        g.fitness=0
        ge.append(g)

    while True:
        
        if not apple_present:
            apple = Apple(block_size)
            apple_present = True

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            # Controls (not needed when AI is implemented)
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT and snake.direction != 'right':
            #         snake.direction = 'left'
            #     if event.key == pygame.K_RIGHT and snake.direction != 'left':
            #         snake.direction = 'right'
            #     if event.key == pygame.K_UP and snake.direction != 'down':
            #         snake.direction = 'up'
            #     if event.key == pygame.K_DOWN and snake.direction != 'up':
            #         snake.direction = 'down'

        screen.fill((0, 0, 0))
        draw_grid(block_size)

        # Draw the apple
        if apple_present:
            pygame.draw.rect(screen, (255, 0, 0), (apple.x, apple.y, block_size, block_size))

        for i, snake in enumerate(snakes):
            t1=time.time()
        # Detect collision
            if snake.collide():
                ge[i].fitness-=1
                snakes.pop(i)
                nets.pop(i)
                ge.pop(i)
                # pygame.quit()
                # exit()

            # Draw snake's body
            for square in snake.body:
                if square == snake.head:
                    pygame.draw.rect(screen, (0, 255, 0), (square[0], square[1], block_size, block_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 0), (square[0], square[1], block_size, block_size))

            output=nets[i].activate(((snake.head[0]-apple.x)**2, (snake.head[1]-apple.y)**2, time.time()-t1))
            
            # Movement
            print(output[0])
            if output[0]<0.5:
                snake.left()
            elif output[0]< 1.5:
                snake.right()
            elif output[0]<2.5:
                snake.down()
            else:
                snake.up()
            
        # # Movement(not needed when AI is implemented)
        # if snake.direction == 'left':
        #     snake.left()
        # elif snake.direction == 'right':
        #     snake.right()
        # elif snake.direction == 'up':
        #     snake.up()
        # elif snake.direction == 'down':
        #     snake.down()
        # snake.body.append(list(snake.head))
        # Eat apple
            if snake.head == [apple.x, apple.y]:
                apple_present = False
                ge[i].fitness+=2
                del apple
            else:
                # if doesn't finds the apple, gets negative reward
                ge[i].fitness-=0.1
                # snake.body.pop(0)

            if len(snakes)==0:
                break
            text = STAT_FONT.render('Score: ' + str(len(snake.body) - 3), 1, (255, 255, 0))
            screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(20)


def run(config_path):
    config=neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population=neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))

    stats=neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


local_dir=os.path.dirname(__file__)
config_path= os.path.join(local_dir, 'config-feedforward.txt')


run(config_path)

