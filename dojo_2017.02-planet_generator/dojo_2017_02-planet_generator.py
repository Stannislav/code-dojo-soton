#!/usr/bin/env python3

import pygame


background_colour = (0, 0, 0)
(width, height) = (600, 400)


class Particle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5, 0)

    def update(self):
        self.x += 1


particles = [Particle(100, 100), Particle(300, 50)]


def draw_main(screen):
    pygame.draw.circle(screen, (255, 0, 0), (width / 2, height / 2), 40, 0)
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
