import pygame
import engine
import scenes
import random

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

	def add_entity(self, ent):
		self.entities_to_add.append(ent)

	def add_entities(self, ents):
		for e in ents:
			self.add_entity(e)

	def __init__(self):
		self.balls = dict()
		self.paddles = dict()
		self.entities = dict()

		self.entities_to_add = []
		self.entities_to_remove = []

		self.cur_entity_id = 0
		
		# Temporarily create all of the surfaces right here so we can test them

		self.temp_ball = Ball()
		self.temp_ball.set_velocity(100,150)
		self.temp_ball.set_position(400,300)

		self.temp_paddle = Paddle()
		self.temp_paddle.set_position(100,500)

		self.temp_brick = Brick()
		self.temp_brick.set_position(100,100)

		self.temp_wall = Wall(100,100)
		self.temp_wall.set_position(500,100)

		self.add_entities([self.temp_ball,self.temp_paddle,self.temp_brick,self.temp_wall])

	def get_next_entity_id(self):
		self.cur_entity_id += 1
		return self.cur_entity_id - 1

	def add_and_remove_pending_entities(self):
		for e in self.entities_to_add:
			ID = self.get_next_entity_id()
			e.set_id(ID)
			self.entities[ID] = e

			if(type(e) is Paddle):
				self.paddles[ID] = e

			if(type(e) is Ball):
				self.balls[ID] = e

		for ID in self.entities_to_remove:
			if ID in self.entities:
				del self.entities[ID]
			if ID in self.paddles:
				del self.paddles[ID]
			if ID in self.balls:
				del self.balls[ID]

		del self.entities_to_add[:]
		del self.entities_to_remove[:]

	def remove_entity_by_id(self, entity_id):
		self.entities_to_remove.append(entity_id)

	def remove_entity(self, ent):
		self.remove_entity_by_id(ent.get_id())

	def do_collision_queue(self):
		return

	def update(self, delta):
		for _,e in self.entities.items():
			e.update(delta)

		self.do_collision_queue()

		self.add_and_remove_pending_entities()


		# Make a small explosion
		if(engine.was_key_pressed(pygame.K_SPACE)):
			px = random.randint(200,600)
			py = random.randint(200,400)
			for i in range(10):
				vx = random.randint(-300,300)
				vy = random.randint(-300,300)

				e = Ball()
				e.set_position(px,py)
				e.set_velocity(vx,vy)
				self.add_entity(e)


		# Clean up the explosion
		if(engine.was_key_pressed(pygame.K_d) and len(self.entities.keys()) > 0):
			for i in range(5):
				entity_id = random.choice(list(self.entities.keys()))
				self.remove_by_entity_id(entity_id)

		#press escape to pause
		if engine.was_key_pressed(pygame.K_ESCAPE): self.pause()


	def render(self, surface):

		surface.fill((100,100,100))
		
		for _,e in self.entities.items():
			e.draw(surface)


	def pause(self):
		engine.add_scene(scenes.PauseScene())
