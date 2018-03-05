import pygame
import engine
import scenes

# This is a subclass of Entity, which means that it behaves just like an entity would in terms of the interface
# Entity is considered to be the "Base" class, like how Pet would be the base class of Cat
# We can treat it exactly like an entity, and call the same functions (set_position, update, intersects, etc)
# It just might have a different implementation of those functions and do something differently when called
class Ball(engine.Entity):

	def __init__(self):
		surf = pygame.Surface((15,15))
		surf.fill((255,255,255))
		#call Entity __init__
		super(type(self),self).__init__(surf)


	# Temporary behavior that has it bouncing along walls and stuff
	def behavior(self):
		if(self.x <= 0 or self.x >= 800):
			self.set_velocity(-self.vx,  self.vy)

		if(self.y <= 0 or self.y >= 600):
			self.set_velocity( self.vx, -self.vy)

class Paddle(engine.Entity):

	def __init__(self):
		surf = pygame.Surface((100,30))
		surf.fill((255,255,255))
		#call Entity __init__
		super(type(self),self).__init__(surf)

	# implement player controls
	def behavior(self):
		return

	def collide_with_ball(self, ball):
		return

class Brick(engine.Entity):

	def __init__(self):
		surf = pygame.Surface((40,15))
		surf.fill((255,0,0))
		#call Entity __init__
		super(type(self),self).__init__(surf)

	def collide_with_ball(self, ball):
		return

class Wall(engine.Entity):

	def __init__(self, width, height):
		surf = pygame.Surface((width,height))
		surf.fill((128,128,128))
		#call Entity __init__
		super(type(self),self).__init__(surf)

	# Reflect ball with same function as brick
	def collide_with_ball(self, ball):
		return

	# prevent paddle from moving past/have it bounce off
	def collide_with_paddle(self, paddle):
		return

# class state should have an update and render function
class PlayScene(engine.Scene):

	def __init__(self):
		self.balls = []
		self.paddles = []
		self.entities = []
		
		# Temporarily create all of the surfaces right here so we can test them

		self.tempBall = Ball()
		self.tempBall.set_velocity(100,150)
		self.tempBall.set_position(400,300)

		self.tempPaddle = Paddle()
		self.tempPaddle.set_position(100,500)

		self.tempBrick = Brick()
		self.tempBrick.set_position(100,100)

		self.tempWall = Wall(100,100)
		self.tempWall.set_position(500,100)


		self.balls.append(self.tempBall)
		self.paddles.append(self.tempPaddle)
		self.entities.extend([self.tempBall,self.tempPaddle,self.tempBrick,self.tempWall])


	def update(self, delta):
		for e in self.entities:
			e.update(delta)
		#press escape to pause
		if engine.was_key_pressed(pygame.K_ESCAPE): self.pause()


	def render(self, surface):

		surface.fill((100,100,100))
		
		for e in self.entities:
			e.draw(surface)


	def pause(self):
		engine.add_scene(scenes.PauseScene())
