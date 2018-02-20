import pygame
import math
from pygame.locals import *
from engine import *

# This is a subclass of Entity, which means that it behaves just like an entity would in terms of the interface
# Entity is considered to be the "Base" class, like how Pet would be the base class of Cat
# We can treat it exactly like an entity, and call the same functions (setPosition, update, intersects, etc)
# It just might have a different implementation of those functions and do something differently when called
class Ball(Entity):

	def __init__(self):
		surf = pygame.Surface((15,15))
		surf.fill((255,255,255))
		Entity.__init__(self, surf)


	# Temporary behavior that has it bouncing along walls and stuff
	def behavior(self):
		if(self.x <= 0 or self.x >= 800):
			self.setVelocity(-self.vx,  self.vy)

		if(self.y <= 0 or self.y >= 600):
			self.setVelocity( self.vx, -self.vy)

class Paddle(Entity):

	def __init__(self):
		surf = pygame.Surface((100,30))
		surf.fill((255,255,255))
		Entity.__init__(self, surf)

	# implement player controls
	def behavior(self):
		return

	def collideWithBall(self, ball):
		return

class Brick(Entity):

	def __init__(self):
		surf = pygame.Surface((40,15))
		surf.fill((255,0,0))
		Entity.__init__(self, surf)

	def collideWithBall(self, ball):
		return

class Wall(Entity):

	def __init__(self, width, height):
		surf = pygame.Surface((width,height))
		surf.fill((128,128,128))
		Entity.__init__(self, surf)

	# Reflect ball with same function as brick
	def collideWithBall(self, ball):
		return

	# prevent paddle from moving past/have it bounce off
	def collideWithPaddle(self, paddle):
		return

# class state should have an update and render function
class PlayScene(Scene):

	def __init__(self):
		self.paused = False

		self.balls = []
		self.paddles = []
		self.entities = []
		
		# Temporarily create all of the surfaces right here so we can test them

		self.tempBall = Ball()
		self.tempBall.setVelocity(100,150)
		self.tempBall.setPosition(400,300)

		self.tempPaddle = Paddle()
		self.tempPaddle.setPosition(100,500)

		self.tempBrick = Brick()
		self.tempBrick.setPosition(100,100)

		self.tempWall = Wall(100,100)
		self.tempWall.setPosition(500,100)


		self.balls.append(self.tempBall)
		self.paddles.append(self.tempPaddle)
		self.entities.extend([self.tempBall,self.tempPaddle,self.tempBrick,self.tempWall])


		self.background = pygame.Surface((800,600))
		self.background.fill((0,0,0))


	def update(self, delta):
		if not self.paused:
			for e in self.entities:
				e.update(delta)



	def render(self):

		screen.blit(self.background,self.background.get_rect())
		
		for e in self.entities:
			e.draw()


	def pause(self):
		self.paused = True


	def resume(self):
		self.paused = False