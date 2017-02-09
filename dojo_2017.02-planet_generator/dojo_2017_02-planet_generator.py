#!/usr/bin/env python3

import pygame
import random


background_colour = (0, 0, 0)
particle_color = (255, 255, 255)
sun_color = (255, 0, 0)
(width, height) = (600, 400)


class Sun():
    def __init__(self, x, y, G):
        self.x = x
        self.y = y
        self.G = G

    def draw(self, screen):
        pygame.draw.circle(screen, sun_color,
                           (int(self.x), int(self.y)), 15 * self.G, 0)


class Particle():
    def __init__(self, x, y, sun):
        self.x = x
        self.y = y
        self.vx = random.random() * 4 - 2
        self.vy = random.random() * 4 - 2
        self.ax = 0
        self.ay = 0.2
        self.sun = sun

    def draw(self, screen):
        pygame.draw.circle(screen, particle_color,
                           (int(self.x), int(self.y)), 5, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay


sun = Sun(width / 2, height / 2, 1)
particles = [Particle(100, 100, sun), Particle(300, 50, sun)]


def draw_main(screen):
    sun.draw(screen)
    for p in particles:
        p.draw(screen)
        p.update()


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
