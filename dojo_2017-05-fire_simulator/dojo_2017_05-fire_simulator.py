#!/usr/bin/env python3

import pygame
import random
import math


background_colour = (0, 0, 0)
(width, height) = (800, 600)
clock = None
fps = 120

fire = None

# colours
red_value = 0
green_value = 0
blue_value = 0
colours = {}
for index in range(80):
    colour = (red_value, green_value, blue_value)
    colours[index] = colour
    if index < 50:
        red_value += 5
        green_value += 2
    else:
        green_value += 2
        blue_value += 5

for index in range(21):
    colours[80+index] = colour

colours[0] = (0, 0, 0)

class Fire(object):
    def __init__(self):
        self.scale = 2
        self.posx = 0
        self.posy = height
        self.sizex = width/self.scale
        self.sizey = 50 #int(1.0*self.posy/self.scale)
        self.grid = [[0]*self.sizex for i in range(self.sizey)]


    def update(self):
        for y in range(self.sizey-1, 0, -1):
            for x in range(1, self.sizex-1):
                self.grid[y][x] = sum(self.grid[y-1][x-1:x+2])//3*99//100
        for x in range(1, self.sizex-1):
            if random.random() < 0.05:
                self.grid[0][x] = 99 - self.grid[0][x]

    def click(self):
        for x in range(1, self.sizex-1):
            self.grid[0][x] = 99



    def draw(self, screen):
        for y in range(1, self.sizey):
            for x in range(self.sizex):
                pygame.draw.rect(
                    screen,
                    colours[self.grid[y][x]],
                    (self.posx + self.scale*x, self.posy - self.scale*y, self.scale, self.scale),
                )


def draw_main(screen):
    clock.tick(fps)

    fire.draw(screen)
    fire.update()

def main():
    global clock, fire

    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('Fireworks')
    clock = pygame.time.Clock()


    # initialize fire
    fire = Fire()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                fire.click()

        # drawing routines
        screen.fill(background_colour)
        draw_main(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
