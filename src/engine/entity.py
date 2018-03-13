import pygame
import engine

# Base class for all objects in the scene, including balls, bricks, and walls
class Entity:

	def __init__(self, image):
		self.sprite = pygame.sprite.Sprite()
		self.sprite.image = image

		# bounding box for this Entity is considered to be equivalent the bounding box for the sprite
		self.bounds = self.sprite.image.get_rect()
		#self.bounds = engine.SRect.fromRect(self.sprite.image.get_rect())

		# These two variables store x and y continuously (float), while bounds only stores integer precision (it's dumb but i didn't write pygame)
		self.x = self.bounds.x
		self.y = self.bounds.y

		self.set_velocity(0,0)

		self.set_id(-1)


	def set_position(self, x, y):
		self.x = x
		self.y = y

		self.bounds.x = x
		self.bounds.y = y

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

		self.bounds.x = self.x
		self.bounds.y = self.y


	def set_velocity(self, vx, vy):
		self.vx = vx
		self.vy = vy

	def set_id(self, entity_id):
		self.entity_id = entity_id



	# Generic update function that handles velocity and stuff
	# Should not be overwritten
	def update(self, delta):
		self.move(delta*self.vx, delta*self.vy)
		self.behavior()



	def draw(self, surface):
		surface.blit(self.sprite.image, self.bounds)
		#surface.blit(self.sprite.image, self.bounds.toRect())


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
	def collide_with_ball(self, ball):
		return

	def collide_with_paddle(self, paddle):
		return