import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 900))
pygame.display.set_caption('Snake')


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        pygame.display.update()

main()