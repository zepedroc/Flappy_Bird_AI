import os
from time import time
import pygame
import neat
import time
import os
import random

from bird import Bird
from floor import Base
from pipe import Pipe

pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

# doubling the size of the images
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'bg.png')))

STAT_FONT = pygame.font.SysFont('comicsans', 50)


def draw_window(win, bird, pipes, base, score):
    # draw background image at position 0,0
    win.blit(BG_IMG, (0, 0))

    # draw the score
    text = STAT_FONT.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 50 - text.get_width(), 10))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # game window
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(30)
        base.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird.jump()

        add_pipe = False
        remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            # if pipe is no longer on the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            # if bird already passed the pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        # add a new pipe to the game
        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        # remove pipes that already passed
        for r in remove:
            pipes.remove(r)

        # if the bird hits the floor
        if bird.y + bird.img.get_height() > 730:
            pass

        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()  # quit python program


main()
