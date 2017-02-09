#!/usr/bin/env python3

import pygame
import random
import math


background_colour = (0, 0, 0)
n_particles = 100
n_suns = 3
(width, height) = (600, 400)


class Sun():
    def __init__(self, x, y, M):
        self.x = int(x)
        self.y = int(y)
        self.color = (255, 0, 0) if M > 0 else (0, 0, 255)
        self.r = int(1 + abs(M))
        self.M = M

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.x, self.y), self.r, 0)


class Particle():
    def __init__(self, x, y, m, suns):
        self.x = x
        self.y = y
        self.vx = random.random() * 4 - 2
        self.vy = random.random() * 4 - 2
        # self.vx = self.vy = 0
        self.ax = 0
        self.ay = 0
        self.r = int(1 + abs(m) / 10)
        self.m = m
        self.suns = suns
        self.dead = False
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.r, 0)

    def update(self):
        if self.dead:
            return

        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay

        self.ax = 0
        self.ay = 0
        for sun in self.suns:
            dx = self.x - sun.x
            dy = self.y - sun.y
            d = math.sqrt(dx * dx + dy * dy)
            if d < self.r + sun.r:
                self.dead = True
                self.color = (255, 255, 0)
            alpha = math.atan2(dy, dx)
            self.ax += -0.5 * self.m * sun.M * math.cos(alpha) / (d * d)
            self.ay += -0.5 * self.m * sun.M * math.sin(alpha) / (d * d)


sun = Sun(width / 2, height / 2, 5)
suns = []
for i in range(n_suns):
    x = random.random() * width / 2 + width / 4
    y = random.random() * height / 2 + width / 4
    M = random.random() * 30 - 15
    suns.append(Sun(x, y, M))

particles = []
for i in range(n_particles):
    x = random.random() * width
    y = random.random() * height
    m = random.random() * 30
    particles.append(Particle(x, y, m, suns))


def draw_main(screen):
    for sun in suns:
        sun.draw(screen)

    for p in particles:
        p.draw(screen)
        p.update()
        if p.dead:
            particles.remove(p)


def main():
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('Planets')

# main loop
    running = True
    while running:
        # events for window closing
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
