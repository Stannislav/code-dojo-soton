#!/usr/bin/env python3

import pygame
import random
import math


background_colour = (0, 0, 0)
(width, height) = (800, 600)
clock = None
fps = 60
G = 0.06


class Particle(object):
    def __init__(self, x, y, v, angle):
        self.x = x
        self.y = y
        self.vx = v * math.sin(angle)
        self.vy = v * math.cos(angle)
        self.ax = 0
        self.ay = 0
        self.r = 1
        self.dead = False
        self.lifetime = -1
        self.color = pygame.Color(255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.r, 0)

    def update(self):
        if not self.dead:
            self.x = self.x + self.vx
            self.y = self.y + self.vy

            self.vx = self.vx + self.ax
            self.vy = self.vy + self.ay + G

            self.lifetime = self.lifetime - 1
            if self.lifetime < 0:
                self.dead = True


class Bullet(Particle):
    def __init__(self, x, y, angle):
        super(Bullet, self).__init__(
            x, y, -8, angle + random.random() * 0.3 - 0.15)
        self.lifetime = 90 - random.randint(0, 20)
        self.exploded = False
        self.dead = False

    # def update(self):
    #     self.y = self.y + self.v
    #     self.lifetime = self.lifetime - 1

    def explode(self):
        self.exploded = True


class Spark(Particle):
    """ Fireworks sparks """
    def __init__(self, x, y, v, angle, hue):
        super(Spark, self).__init__(x, y, v, angle)
        self.lifetime = 60
        self.color = pygame.Color(0, 0, 0)
        self.color.hsva = (hue, 100, 100, 100)

        self.prev_pos = []
        self.trail = 20

    def update(self):
        super(Spark, self).update()
        hsva = list(self.color.hsva)
        hsva[2] = hsva[2] - 1
        if hsva[2] < 0:
            hsva[2] = 0
        self.color.hsva = tuple(map(int, hsva))

        # store position history for trail
        self.prev_pos.append((self.x, self.y))
        if len(self.prev_pos) > self.trail:
            self.prev_pos = self.prev_pos[-self.trail:]

    def draw(self, screen):
        super(Spark, self).draw(screen)
        # draw the trail
        for i, p in enumerate(self.prev_pos):
            pygame.draw.circle(screen, self.color,
                               (int(p[0]), int(p[1])), self.r, 0)


bullets = [Bullet(random.randint(0, width), height, 0)]
sparks = []


def draw_main(screen):
    clock.tick(fps)

    # pygame.draw.line(screen, (0, 255, 255), (100, 100), (400, 400))
    # pygame.draw.circle(screen, (255, 255, 255), (300, 300), 4, 0)

    if random.random() < 0.1:
        bullets.append(Bullet(random.randint(0, width), height, 0))

    for b in bullets:
        if not b.dead:
            b.update()
            b.draw(screen)
            if b.lifetime == 0:
                b.explode()
                hue = random.random() * 360
                n = 20
                for i in range(n):
                    sparks.append(
                        Spark(b.x, b.y, 2, 2.0 * math.pi * i / n, hue))
        else:
            bullets.remove(b)

    for s in sparks:
        if not s.dead:
            s.update()
            s.draw(screen)
        else:
            sparks.remove(s)


def main():
    global clock
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('Fireworks')
    clock = pygame.time.Clock()

    # main loop
    running = True
    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                mods = pygame.key.get_mods()
                if keys[pygame.K_ESCAPE] or \
                   (keys[pygame.K_w] and mods & pygame.KMOD_META):
                    running = False

        # drawing routines
        screen.fill(background_colour)
        draw_main(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
