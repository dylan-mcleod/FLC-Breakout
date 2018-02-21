import pygame

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



	def draw(self, surface):
		surface.blit(self.sprite.image, self.bounds)


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