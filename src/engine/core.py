import pygame
import math

pygame.init()
#Make an 800x600 window
gameScreen = pygame.display.set_mode((800, 600))


#Scene - a part of the game, such as the main menu or play screen.
#these can also be individual levels
class Scene:

	def __init__(self):
		"""Called on scene creation."""
		pass

	def __del__(self):
		"""Called on scene deletion (garbage collection). Here for debugging."""
		print("Scene %s deleted." % self.__class__.__name__)

	def update(self, delta):
		"""Update scene objects, check user input, etc."""
		print("Scene %s has no update method!" % self.__class__.__name__)

	def render(self):
		"""Render scene objects, buttons, text, etc."""
		print("Scene %s has no render method!" % self.__class__.__name__)

	def pause(self):
		"""Called when an external object wants the game to pause, like when FPS is too low."""
		pass

	#future possibility
	#def resize(self,resolution)

#Handles Scenes and gameloop
class SceneManager:

	#Here for organization purposes. May be temporary.
	class SafeExit(Exception):
		pass

	def __init__(self):

		self.scenes = []
		self.screens = []

		self.targetFPS = 60
		self.minFPS = 15
		self.clock = pygame.time.Clock()

	
	def addScene(self, scene):
		"""Adds a scene to the stack, useful in pause menus."""
		
		#push the scene to the stack without replacing the top
		self.scenes.append(scene)
		self.screens.append(pygame.Surface(gameScreen.get_size(),pygame.SRCALPHA))

	def switchScene(self, scene):
		"""Switches current scene to another. Keeps stack."""

		#get out of old scene
		self.exitScene()
		#add new scene
		self.addScene(scene)


	def replaceScene(self, scene):
		"""Replaces current scenes with a scene. Clears stack."""

		#get out of old scene
		while self.scenes:
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
		screen = self.screens.pop()
		#destroy the scene (here for future reference)
		#scene.destroy()


	def run(self,scene = None):
		"""Starts the game, with an optional starting scene."""

		#start at provided scene if it exists
		if(scene):
			self.switchScene(scene)
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
		#self.scenes = []
		exit()


	def main_loop(self):
		"""The main game loop."""

		while(self.scenes):
			# ticks targetFPS times per second, divided by 1000 to convert ms to s
			delta = self.clock.tick(self.targetFPS) / 1000.0

			if not self.scenes:
				raise SafeExit("scene stack empty")
			#protection against extremely low fps; pause if fps is below 
			if delta > (1.0 / self.minFPS):
				self.scenes[-1].pause()

			#only update and render current (top/focused) scene

			#try to update the current scene
			self.scenes[-1].update(delta)
			#render the current scene
			self.scenes[-1].render(self.screens[-1])

			#render all scenes on top of one another
			for curscreen in self.screens:
				gameScreen.blit(curscreen, curscreen.get_rect())
			# Call this to send whatever has been rendered on screen over to the monitor
			pygame.display.flip()

			#update inputs
			keyboardManager.update()
			mouseManager.update()

			#process events
			self.event_handler()
		raise self.SafeExit("no more scenes")

	def event_handler(self):
		"""Handles events from pygame"""

		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				raise self.SafeExit("window closed")
			#the python equivalent of a switch statement
			{
				pygame.MOUSEBUTTONUP : mouseManager.upEvent,
				pygame.MOUSEBUTTONDOWN : mouseManager.downEvent,
				pygame.KEYDOWN : keyboardManager.downEvent,
				pygame.KEYUP : keyboardManager.upEvent,
				pygame.JOYAXISMOTION : gamepadManager.JOYAXISMOTION,
				pygame.JOYBALLMOTION : gamepadManager.JOYBALLMOTION,
				pygame.JOYHATMOTION : gamepadManager.JOYHATMOTION,
				pygame.JOYBUTTONUP : gamepadManager.JOYBUTTONUP,
				pygame.JOYBUTTONDOWN : gamepadManager.JOYBUTTONDOWN
			}.get(evt.type, self.emptyEventCallback)(evt)

	def emptyEventCallback(self, evt):
		"""Intentionally does nothing."""
		pass


#Manages mouse events.
#Could use a lot of additional features, especially for buttons.
class MouseManager:

	def __init__(self):
		self.mouseClicks = [[],[],[],[],[],[],[]]
		self.mouseDowns = [(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)]

	def update(self):
		self.mouseClicks = [[],[],[],[],[],[],[]]

	def downEvent(self, evt):
		self.mouseDowns[evt.button - 1] = evt.pos

	def upEvent(self, evt):
		btn = evt.button - 1
		if(evt.pos == self.mouseDowns[btn]):
			self.mouseClicks[btn].append(evt.pos)

	def getClicks(self):
		return self.mouseClicks


#Manages the keyboard.
#Could use some additions/modifications.
class KeyboardManager:

	def __init__(self):
		#pygame.key.set_repeat(None) called during pygame init
		self.state = pygame.key.get_pressed()
		self.pressed = [False] * 512

	def update(self):
		self.state = pygame.key.get_pressed()
		self.pressed = [False] * 512

	def downEvent(self, evt):
		pass

	def upEvent(self, evt):
		self.pressed[evt.key] = True

	def isKeyDown(self, key):
		return self.state[key]

	def wasKeyPressed(self, key):
		return self.pressed[key]

#Manages gamepad events.
#Not yet implemented.
class GamepadManager:

	def __init__(self):
		pass

	def update(self):
		pass

	def JOYAXISMOTION(self, evt):
		pass

	def JOYBALLMOTION(self, evt):
		pass

	def JOYHATMOTION(self, evt):
		pass

	def JOYBUTTONUP(self, evt):
		pass

	def JOYBUTTONDOWN(self, evt):
		pass


mouseManager = MouseManager()
keyboardManager = KeyboardManager()
gamepadManager = GamepadManager()
sceneManager = SceneManager()