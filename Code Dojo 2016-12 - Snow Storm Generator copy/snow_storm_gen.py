#!/usr/bin/env python

import pygame
import random
import math

background_colour = (0,0,0)
(width, height) = (600, 400)
wind = random.random()*2-1
def_size = 5

class Flake():
	def __init__(self, screen, x_y, size):
		self.screen = screen
		self.x, self.y = x_y
		self.size = size
		self.colour = (255, 255, 255)
		self.thickness = 1
		self.speed = 2+random.random()
		self.wind = wind
		self.stopped = False
		self.intspeed=random.random()*0.2-0.1
		self.intangle=0
		self.wobbleangle=0
		self.wobbleamp=1
		self.wobblespeed=0.3

	def display(self):
		pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size/2, self.thickness)
		for n in range(3):
			angle = n*math.pi/3 + self.intangle
			pygame.draw.line(self.screen, self.colour,
				(int(self.x-self.size*math.cos(angle)), int(self.y-self.size*math.sin(angle))),
				(int(self.x+self.size*math.cos(angle)), int(self.y+self.size*math.sin(angle))), self.thickness)

	def move(self):
		self.intangle += self.intspeed
		self.angle = 3/2*math.pi + self.wind*math.pi/4
		self.wobbleangle += self.wobblespeed
		self.x += math.sin(self.angle) * self.speed + math.sin(self.wobbleangle)*self.wobbleamp
		self.y -= math.cos(self.angle) * self.speed

def change_wind():
	global wind
	if random.randint(0,100) == 0:
		wind = random.random()*2-1
		for flake in my_flakes:
			flake.wind = wind

def draw_snowman(screen):
	pygame.draw.circle(screen, (255,255,255), (width/4, height-20), 40, 0)
	pygame.draw.circle(screen, (255,255,255), (width/4, height-75), 30, 0)
	pygame.draw.circle(screen, (255,255,255), (width/4, height-115), 20, 0)
	pygame.draw.line(screen, (100,50,0),(width/4-20, height-85),(width/4-50, height-100), 3)
	pygame.draw.line(screen, (100,50,0),(width/4+20, height-85),(width/4+50, height-100), 3)
	pygame.draw.circle(screen, (0,0,0), (width/4-10, height-120), 2, 0)
	pygame.draw.circle(screen, (0,0,0), (width/4+10, height-120), 2, 0)

def draw_main(screen):
	global my_flakes
	# change wind
	change_wind()
	# add new flakes
	if random.randint(0,1) == 0:
		my_flakes += [Flake(screen, (random.randint(0,3*width)-width,-10-random.randint(0,20)), def_size) for i in range(5)]
	# draw all flakes
	for i,flake in enumerate(my_flakes):
		if flake.y > height:
			del my_flakes[i]
			continue
		flake.move()
		flake.display()
	# draw the snowman
	draw_snowman(screen)

my_flakes = []
def main():
# initialize pygame
	pygame.init()
	screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
	pygame.display.set_caption('Snow Flakes')

# some settings
	number_of_particles = 50

# generate initial flakes
	for n in range(number_of_particles):
		x = random.randint(0,3*width)-width
		flake = Flake(screen, (x,0), def_size)
		my_flakes.append(flake)

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
				if keys[pygame.K_ESCAPE] or (keys[pygame.K_w] and mods&pygame.KMOD_META):
					running = False
# drawing routines
		screen.fill(background_colour)
		draw_main(screen)
		pygame.display.flip()
	pygame.quit()

if __name__ == '__main__':
	main()
