import pygame
import os
import time
import neat
import random


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        #initializing bird atributes
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        displace = self.velocity * self.tick_count + 1.5 * self.tick_count**2 #acceleration equation
        
        if displace >= 16: #termination velocity or max velocity possible
            displace = 16
        
        if displace < 0:
            displace -= 2

        self.y = self.y + displace

        if displace < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt >= -90:
                self.tilt -= self.ROTATION_VEL

    def draw(self, canvas):
        self.img_count += 1

        #flapping animation with the different bird imgs
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft= (self.x, self.y)).center)
        canvas.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mas.from_surface(self.img)


def draw_canvas(canvas, bird):
    #draw in canvas
    canvas.blit(BG_IMG, (0, 0))
    bird.draw(canvas)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    canvas = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_canvas(canvas, bird)

    pygame.quit()
    quit()
        
main()