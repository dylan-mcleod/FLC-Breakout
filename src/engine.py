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

# class Scene should have an update and render function
class Scene:

	def __init__(self):
		self.paused = False

	def __del__(self):
		print("Scene %s deleted." % self.__class__.__name__)

	def update(self, delta):
		return

	def render(self):
		return

	def pause(self):
		self.paused = True

	def resume(self):
		self.paused = False


# handles Scenes and gameloop
# unfinished, needs some extra stuffs for adding/switching Scenes, as well as Scene base class
class SceneManager:

	class SafeExit(Exception):
		pass

	class NoScenesInStack(SafeExit):
		pass

	class WindowClosed(SafeExit):
		pass

	def __init__(self):
		self.scenes = []

		self.targetFPS = 60
		self.minFPS = 15
		self.clock = pygame.time.Clock()

	
	def addScene(self, scene):
		"""Adds a scene to the stack, useful in pause menus."""

		#push the scene to the stack without replacing the top
		self.scenes.append(scene)


	#Switches current scene to another. Keeps stack.
	def switchScene(self, scene):
		"""Switches current scene to another. Keeps stack."""

		#get out of old scene
		self.exitScene()
		#add new scene
		self.addScene(scene)


	def exitScene(self):
		"""Exits current scene."""

		#protection for empty scene stack
		if not self.scenes:
			return
		#remove current scene from stack
		scene = self.scenes.pop()
		#destroy the scene (here for future reference)
		#scene.destroy()


	def run(self,scene = None):
		#start the timer
		self.clock.tick(60)
		#encompass loop for easy exiting
		try:
			self.main_loop()
		#Safely exited
		except self.SafeExit as error:
			reason = "safe exit"
			print("Exiting game. Reason: %s." % repr(error))
		#Exited on bad terms
		#except Exception as error:
		#	print("Exiting game on bad terms.")
		#	print(repr(error))
		#	print("Press enter to continue.")
		#	input()
		self.scenes = []
		exit()


		#EOL

	def main_loop(self):
		while(self.scenes):
			
			# ticks targetFPS times per second, divided by 1000 to convert ms to s
			delta = self.clock.tick(self.targetFPS) / 1000.0

			if not self.scenes:
				raise SafeExit("scene stack empty")
			#protection against extremely low fps; pause if fps is below 
			if delta > (1.0 / self.minFPS):
				self.scenes[-1].pause()

			#try to update the current scene
			self.scenes[-1].update(delta)

			#surf = pygame.display.get_surface().copy()
			#render the current scene
			self.scenes[-1].render()

			#pygame.surface.blit(surf)
			# Call this to send whatever has been rendered on screen over to the monitor
			pygame.display.flip()


			# Wrong place for this, but this allows us to exit the application so i'm putting it here for now
			if(pygame.event.peek(pygame.QUIT)):
				#self.exit("window closed")
				raise self.SafeExit("window closed")

			for event in pygame.event.get():
				if event.type == KEYDOWN:
					#Here for now
					if event.key == K_SPACE:
						self.scenes[-1].resume()
		#stack empty, program should exit





sceneManager = SceneManager()

def switchScene(scene):
	sceneManager.switchScene(scene)