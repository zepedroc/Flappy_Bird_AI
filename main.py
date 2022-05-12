import os
import pygame
import neat
import os

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


def draw_window(win, birds, pipes, base, score):
    # draw background image at position 0,0
    win.blit(BG_IMG, (0, 0))

    # draw the score
    text = STAT_FONT.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 50 - text.get_width(), 10))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    nets = []  # neural networks
    ge = []  # genomes
    birds = []

    # setting a network for each genome
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

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
                pygame.quit()
                quit()  # quit python program

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            # activate nn with 3 inputs
            output = nets[x].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        remove = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    # remove everything related to that bird
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # if bird already passed the pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # if pipe is no longer on the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            pipe.move()

        # add a new pipe to the game
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5  # reward the birds that went through the pipe
            pipes.append(Pipe(700))

        # remove pipes that already passed
        for r in remove:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            # if the bird hits the floor or the sky
            if bird.y + bird.img.get_height() > 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        # show the fitness instead of the scrore
        fitness = 0
        if len(ge) > 0:
            fitness = ge[0].fitness

        draw_window(win, birds, pipes, base, round(fitness, 1))


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # create population
    p = neat.Population(config)

    # add statistics
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # add fitness function / generations number
    winner = p.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
