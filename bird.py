import pygame
import os

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
               pygame.transform.scale2x(pygame.image.load(
                   os.path.join('imgs', 'bird2.png'))),
               pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]


class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25  # turn the bird up or down by 25º max
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5   # to go up we have to decrease y position
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # equation to move the bird / px per frame / negative means it's going up
        d = self.vel * self.tick_count + 1.5 * \
            self.tick_count**2

        if d >= 16:  # move down 16px per frame at max
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        # tilt the bird
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL  # tilt the bird down until it is nose diving

    def draw(self, win):
        self.img_count += 1

        # draw animation to flap wings
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # if it's nose diving do not flap wings
        if self.tilt == -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotate img around its center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)

        # actually draw it
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
