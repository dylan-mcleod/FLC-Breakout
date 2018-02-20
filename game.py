import pygame
import math
from pygame.locals import *



pygame.init()

# Make an 800x600 window
screen = pygame.display.set_mode((800, 600))



# Base class for all objects in the scene, including balls, bricks, and walls
class Entity:

	def __init__(self, image):
		self.sprite = pygame.sprite.Sprite()
		self.sprite.image = image

		# bounding box for this Entity is considered to be equivalent the bounding box for the sprite
		self.bounds = self.sprite.image.get_rect()

		# These two variables store x and y continuously (float), while bounds only stores integer precision (it's dumb but i didn't write pygame)
		self.x = self.bounds.x
		self.y = self.bounds.y

		self.setVelocity(0,0)


	def setPosition(self, x, y):
		self.x = x
		self.y = y

		self.bounds.x = x
		self.bounds.y = y

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

		self.bounds.x = self.x
		self.bounds.y = self.y


	def setVelocity(self, vx, vy):
		self.vx = vx
		self.vy = vy



	# Generic update function that handles velocity and stuff
	# Should not be overwritten
	def update(self, delta):
		self.move(delta*self.vx, delta*self.vy)
		self.behavior()



	def draw(self):
		screen.blit(self.sprite.image, self.bounds)


	# Super special update function that you can overwrite as you please
	# Used for special behaviors for specific objects
	# Shouldn't need delta, because the update function should take care of anything that necessitates delta
	def behavior(self):
		return

	######################
	# Collision Handling #
	######################

	# Check if this intersects another thing, not implemented
	def intersects(self, other):
		return self.bounds.colliderect(other.bounds)


	# These functions do nothing, they must be implemented by children
	def collideWithBall(self, ball):
		return

	def collideWithPaddle(self, paddle):
		return


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
class GameState:

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






# handles states and gameloop
# unfinished, needs some extra stuffs for adding/switching states, as well as state base class
class StateManager:

	def __init__(self):
		self.states = dict()
		self.currentState = None

		self.targetFPS = 60
		self.minFPS = 15
		self.clock = pygame.time.Clock()

	def addState(self, name, state):
		self.states[name] = state

	def selectState(self, name):
		self.currentState = self.states[name]


	def run(self):
		running = True
		self.clock.tick(60)
		while(running and (not (self.currentState is None))):
			
			# ticks targetFPS times per second, divided by 1000 to convert ms to s
			delta = self.clock.tick(self.targetFPS) / 1000.0
			#protection against extremely low fps
			if delta > (1.0 / self.minFPS):
				self.currentState.pause()

			self.currentState.update(delta)
			self.currentState.render()

			# Call this to send whatever has been rendered on screen over to the monitor
			pygame.display.flip()


			# Wrong place for this, but this allows us to exit the application so i'm putting it here for now
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						running = False
					#Here for now
					if event.key == K_SPACE:
						self.currentState.resume()
				elif event.type == QUIT:
					running = False


hello = StateManager()
hello.addState("game", GameState())
hello.selectState("game")
hello.run()