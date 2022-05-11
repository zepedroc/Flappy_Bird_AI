import os
from time import time
import pygame
import neat
import time
import os
import random

from bird import Bird

WIN_WIDTH = 600
WIN_HEIGHT = 800

# doubling the size of the images

PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'bg.png')))


def draw_window(win, bird):
    # draw background image at position 0,0
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)

    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # game window

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(win, bird)

    pygame.quit()
    quit()  # quit python program


main()
