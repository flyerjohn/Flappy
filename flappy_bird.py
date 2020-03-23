import pygame
import os
import time
import neat
import random
pygame.font.init() #initializing the font module in pyame

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

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
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bot = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOT = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bot = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, canvas):
        canvas.blit(self.PIPE_TOP, (self.x, self.top))
        canvas.blit(self.PIPE_BOT, (self.x, self.bot))

    #pixel colliding method
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bot_mask = pygame.mask.from_surface(self.PIPE_TOP)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bot - round(bird.y))

        b_point = bird_mask.overlap(bot_mask, bot_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False


class Base:
    VELOCITY = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    #'infinite' cycle
    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, canvas):
        canvas.blit(self.IMG, (self.x1, self.y))
        canvas.blit(self.IMG, (self.x2, self.y))


def draw_canvas(canvas, bird, base, pipes, score):
    #draw in canvas
    canvas.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(canvas)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    canvas.blit(text, (CANVAS_WIDTH - 10 - text.get_width(), 10))

    base.draw(canvas)

    bird.draw(canvas)
    pygame.display.update()

#game loop
def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(550)]
    canvas = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #bird.move()
        add_pipe = False

        removed = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(550))

        for r in removed:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            pass

        base.move()
        draw_canvas(canvas, bird, base, pipes, score)

    pygame.quit()
    quit()
        
main()