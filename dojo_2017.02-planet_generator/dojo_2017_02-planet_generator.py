#!/usr/bin/env python3

import pygame
import random
import math


background_colour = (0, 0, 0)
n_particles = 100
n_suns = 3
p_new = None
c_down = None
m_new = None
(width, height) = (800, 600)


class Sun():
    def __init__(self, x, y, M):
        self.x = int(x)
        self.y = int(y)
        self.color = (255, 0, 0) if M > 0 else (0, 0, 255)
        self.r = int(math.ceil(math.sqrt(abs(M))))
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
        self.r = int(math.ceil(math.sqrt(abs(m))))
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

        ax = 0
        ay = 0
        for sun in self.suns:
            dx = self.x - sun.x
            dy = self.y - sun.y
            d = math.sqrt(dx * dx + dy * dy)
            if d < self.r + sun.r:
                self.dead = True
                self.color = (255, 255, 0)
            alpha = math.atan2(dy, dx)
            ax += -0.5 * self.m * sun.M * math.cos(alpha) / (d * d)
            ay += -0.5 * self.m * sun.M * math.sin(alpha) / (d * d)

        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy


suns = []
for i in range(n_suns):
    x = random.random() * width / 2 + width / 4
    y = random.random() * height / 2 + height / 4
    M = random.random() * 100 + 50
    if random.random() < 0.5:
        M = -M
    suns.append(Sun(x, y, M))

particles = []
for i in range(n_particles):
    x = random.random() * width
    y = random.random() * height
    m = random.random() * 10
    particles.append(Particle(x, y, m, suns))


def draw_main(screen):
    for sun in suns:
        sun.draw(screen)

    for p in particles:
        p.draw(screen)
        p.update()
        if p.dead:
            particles.remove(p)

    if p_new:
        p_new.x, p_new.y = pygame.mouse.get_pos()
        p_new.draw(screen)
        pygame.draw.line(screen, (0, 255, 255), c_down, pygame.mouse.get_pos())


def main():
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('Planets')
    global p_new, c_down

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                c_down = pygame.mouse.get_pos()
                m = random.random() * 30
                p_new = Particle(c_down[0], c_down[1], m, suns)
            elif event.type == pygame.MOUSEBUTTONUP:
                c_up = pygame.mouse.get_pos()
                p_new.vx = (c_up[0] - c_down[0]) / 20
                p_new.vy = (c_up[1] - c_down[1]) / 20
                particles.append(p_new)
                p_new = None

        # drawing routines
        screen.fill(background_colour)
        draw_main(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
