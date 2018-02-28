import pygame
import math

#Not sure if this should be here.
pygame.init()
#Here for game engine only - do not use!
gameScreen = pygame.display.set_mode((800, 600))


#Scene - a part of the game, such as the main menu or play screen.
#these can also be individual levels
class Scene:

	def __init__(self):
		"""Called on scene creation."""
		pass

	def __del__(self):
		"""Called on scene deletion (garbage collection). Here for debugging."""
		#print("Scene {} deleted.".format(self.getName()))
		pass

	def getName(self):
		"""Here for naming purposes. Can be overridden for manual control over scene name."""
		return self.__class__.__name__

	def update(self, delta):
		"""Update scene objects, check user input, etc."""
		print("Scene {} has no update method!".format(self.getName()))

	def render(self):
		"""Render scene objects, buttons, text, etc."""
		print("Scene {} has no render method!".format(self.getName()))

	def pause(self):
		"""Called when an external object wants the game to pause, like when FPS is too low."""
		pass

	#future possibilities:
	#def enter(self)
	#def enterFocus(self)
	#def leaveFocus(self)
	#def resize(self, resolution)
	#def exit(self)

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
		print("Scene Manager: Adding {}.".format(scene.getName()))
		self.silentAddScene(scene)

	def switchScene(self, scene):
		"""Switches current scene to another. Keeps stack."""
		print("Scene Manager: Switching from {} to {}.".format(self.scenes[-1].getName() if self.scenes else "<None>", scene.getName()))
		#get out of old scene
		self.silentExitScene()
		#add new scene
		self.silentAddScene(scene)

	def replaceScene(self, scene):
		"""Replaces current scenes with a scene. Clears stack."""
		print("Scene Manager: Replacing to {}.".format(scene.getName()))
		#get out of old scene
		while self.scenes:
			self.silentExitScene()
		#add new scene
		self.silentAddScene(scene)

	def exitScene(self):
		"""Exits current scene."""
		if(not self.scenes):
			return
		print("Scene Manager: Exiting {}.".format(self.scenes[-1].getName()))
		self.silentExitScene()
	
	#Only for internal engine use, due to no debug print statements.
	def silentAddScene(self, scene):
		#push the scene to the stack without replacing the top
		self.scenes.append(scene)
		self.screens.append(pygame.Surface(gameScreen.get_size(),pygame.SRCALPHA))

	#Only for internal engine use, due to no debug print statements.
	def silentExitScene(self):
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
			self.addScene(scene)
		#start the timer
		self.clock.tick(60)
		#encompass loop for easy exiting
		try:
			print(self.main_loop())
			exit()
		#Safely exited
		except self.SafeExit as error:
			reason = "safe exit"
			print("Exiting game. Reason: {}.".format(repr(error)))
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
				print("Scene Manager: Called scene ({}) pause() due to low FPS. Setting highest delta.".format(self.scenes[-1].getName()))
				self.scenes[-1].pause()
				#set delta to highest allowed value for update protection
				delta = 1.0 / self.minFPS

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
			gamepadManager.update()

			#process events
			evt = self.event_handler()
			if(evt):
				return evt
		return "No more scenes."
		#raise self.SafeExit("no more scenes")

	def event_handler(self):
		"""Handles events from pygame"""

		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				#raise self.SafeExit("window closed")
				return "Window closed."
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
#Could use a few additional features, especially for buttons.
class MouseManager:

	def __init__(self):
		self.mouseClicks = [[],[],[],[],[],[],[]]
		self.mouseDowns = [(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)]
		self.virtualModeEnabled = False
		self.relMovement = (0,0)

	def update(self):
		self.mouseClicks = [[],[],[],[],[],[],[]]
		self.relMovement = pygame.mouse.get_rel()
		if(self.virtualModeEnabled):
			self.setMousePosition((0,0))
			#setgameScreen.get_size() / 2

	def downEvent(self, evt):
		self.mouseDowns[evt.button - 1] = evt.pos

	def upEvent(self, evt):
		btn = evt.button - 1
		if(evt.pos == self.mouseDowns[btn]):
			self.mouseClicks[btn].append(evt.pos)

	def getClicks(self):
		"""Returns an array of arrays of tuples of mouse clicks since the last frame"""
		return self.mouseClicks

	def getMousePosition(self):
		"""Returns the current mouse position, as a tuple."""
		return pygame.mouse.get_pos()

	def setMousePosition(self, pos):
		"""Sets the mouse position. Ideally, should only be used with setMouseGrab(True)."""
		return pygame.mouse.set_pos(pos[0], pos[1])

	def getVirtualMode(self):
		"""Returns True if virtual mode is enabled."""
		if((pygame.event.get_grab() != self.virtualModeEnabled) or (pygame.mouse.get_visible() != self.virtualModeEnabled)):
			print("WARNING!: Invalid virtual mode state! Attempting to fix.")
			self.setVirtualMode(self.virtualModeEnabled)
		return pygame.event.get_grab()

	def getMouseMovement(self):
		"""Gets relative mouse movement since last frame."""
		return self.relMovement

	def setVirtualMode(self, grb):
		"""Sets virtual mode (True or False)."""
		print("Virtual mode {}.".format("enabled" if grb else "disabled"))
		pygame.event.set_grab(grb)
		pygame.mouse.set_visible(not grb)
		return self.getVirtualMode()

	def enterVirtualMode(self):
		"""Enters virtual mode."""
		return self.setVirtualMode(True)

	def leaveVirtualMode(self):
		"""Leaves virtual mode."""
		return self.setVirtualMode(False)

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
		"""Returns True if key is currently being pressed."""
		return self.state[key]

	def wasKeyPressed(self, key):
		"""Returns True if the key was pressed last frame."""
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