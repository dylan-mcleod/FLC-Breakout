import pygame
import math
from pygame.locals import *


# Test program, should produce a black window
# with a white square going in circles

pygame.init()

# Make an 800x600 window
screen = pygame.display.set_mode((800, 600))

# Create a drawing surface of size 50
surf = pygame.Surface((50, 50))
surf.fill((255, 255, 255)) # Color it white

background = pygame.Surface((800,600))
background.fill((0,0,0))
background.get_rect().x=0
background.get_rect().y=0

# Position of our drawing surface
rect = surf.get_rect()

# Game loop, set running to False to exit the loop
time = 0
running = True
while running:
	
	# Handle whatever events that have been called, by looping throughzz
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			# If the Esc key has been pressed set running to false to exit the main loop
			if event.key == K_ESCAPE:
				running = False
		# Check for QUIT event; if QUIT, set running to false
		elif event.type == QUIT:
			running = False

	screen.blit(background,background.get_rect())

	rect.x = 400+220*math.cos(time)
	rect.y = 300+220*math.sin(time)
	# This line says "Draw surf onto screen at coordinates x:400, y:300"
	screen.blit(surf, rect)

	time += 0.005
	# Call this every frame to refresh what's been drawn to the screen
	pygame.display.flip()