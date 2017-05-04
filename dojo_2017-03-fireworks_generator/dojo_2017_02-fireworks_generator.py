#!/usr/bin/env python3

import pygame
import random
import math


background_colour = (0, 0, 0)
(width, height) = (800, 600)
clock = None
fps = 60

grav = 0.1
airfric = 0.95
nsparks = 40

bullets = []
sparks = []


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
        self.lifetime = fps  # = 1 second
        self.color = [255, 255, 255]

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.r, 0)

    def update(self):
        if not self.dead:
            self.x = self.x + self.vx
            self.y = self.y + self.vy

            self.vx = self.vx + self.ax
            self.vy = self.vy + self.ay + grav

            self.vx = self.vx * airfric
            self.vy = self.vy * airfric

            self.lifetime = self.lifetime - 1
            if self.lifetime < 0:
                self.dead = True


class Bullet(Particle):
    def __init__(self, x, y):
        super(Bullet, self).__init__(
            x, y, -25, random.random() * 0.3 - 0.15)

        self.lifetime = 70 - random.randint(0, 60)
        self.dead = False
        self.color = [0x88] * 3


class Spark(Particle):
    def __init__(self, x, y, v, angle, hue):
        super(Spark, self).__init__(x, y, v, angle)

        self.lifetime = 120
        c = pygame.Color(0)
        c.hsva = (hue, 100, 100, 100)
        self.color = [c.r, c.g, c.b]
        self.fade = 3

        self.prev_pos = []
        self.trail = 20

    def update(self):
        super(Spark, self).update()

        # fade the color at each update
        self.color = [v - self.fade for v in self.color]
        self.color = [v if v > 0 else 0 for v in self.color]

        # store position history for trail
        self.prev_pos.append((self.x, self.y))
        if len(self.prev_pos) > self.trail:
            self.prev_pos = self.prev_pos[-self.trail:]

    def draw(self, screen):
        super(Spark, self).draw(screen)
        # draw the trail
        c = list(self.color)
        for i, p in enumerate(self.prev_pos):
            pygame.draw.circle(screen, [v * i / self.trail for v in c],
                               (int(p[0]), int(p[1])), int(self.r * 0.75), 0)


def draw_main(screen):
    clock.tick(fps)

    # randomly generate new fireworks
    if random.random() < 0.05:
        bullets.append(Bullet(random.randint(0, width), height))

    # iterate through bullets
    for b in bullets:
        if b.dead:
            bullets.remove(b)
        else:
            b.update()
            b.draw(screen)
            # bullet about to die - explode!
            if b.lifetime == 1:
                hue = random.random() * 360
                for i in range(nsparks):
                    sparks.append(Spark(
                        b.x, b.y, 5 + random.random(),
                        2.0 * math.pi * i / nsparks, hue))

    # iterate through sparks
    for s in sparks:
        if s.dead:
            sparks.remove(s)
        else:
            s.update()
            s.draw(screen)


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
