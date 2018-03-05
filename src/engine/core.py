import pygame
import math
import engine.graphics

#Not sure if this should be here.
pygame.init()

#set the window caption
pygame.display.set_caption("Breakout!")
#set the window icon
#pygame.display.set_icon(surface)
starting_size = (1280, 720)
#Here for game engine only - do not use!
gameScreen = pygame.display.set_mode(starting_size, pygame.RESIZABLE)
engine.graphics.resize(starting_size)


#Scene - a part of the game, such as the main menu or play screen.
#these can also be individual levels
class Scene:

	def __init__(self):
		"""Called on scene creation."""
		pass

	def __del__(self):
		"""Called on scene deletion (garbage collection). Here for debugging."""
		#print("Scene {} deleted.".format(self.get_name()))
		pass

	def get_name(self):
		"""Here for naming purposes. Can be overridden for manual control over scene name."""
		return self.__class__.__name__

	def update(self, delta):
		"""Update scene objects, check user input, etc."""
		print("Scene {} has no update method!".format(self.get_name()))

	def render(self):
		"""Render scene objects, buttons, text, etc."""
		print("Scene {} has no render method!".format(self.get_name()))

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
	
	def add_scene(self, scene):
		"""Adds a scene to the stack, useful in pause menus."""
		print("Scene Manager: Adding {}.".format(scene.get_name()))
		self.silent_add_scene(scene)

	def switch_scene(self, scene):
		"""Switches current scene to another. Keeps stack."""
		print("Scene Manager: Switching from {} to {}.".format(self.scenes[-1].get_name() if self.scenes else "<None>", scene.get_name()))
		#get out of old scene
		self.silent_exit_scene()
		#add new scene
		self.silent_add_scene(scene)

	def replace_scene(self, scene):
		"""Replaces current scenes with a scene. Clears stack."""
		print("Scene Manager: Replacing to {}.".format(scene.get_name()))
		#get out of old scene
		while self.scenes:
			self.silent_exit_scene()
		#add new scene
		self.silent_add_scene(scene)

	def exit_scene(self):
		"""Exits current scene."""
		if(not self.scenes):
			return
		print("Scene Manager: Exiting {}.".format(self.scenes[-1].get_name()))
		self.silent_exit_scene()
	
	#Only for internal engine use, due to no debug print statements.
	def silent_add_scene(self, scene):
		#push the scene to the stack without replacing the top
		self.scenes.append(scene)
		self.screens.append(pygame.Surface(gameScreen.get_size(),pygame.SRCALPHA))

	#Only for internal engine use, due to no debug print statements.
	def silent_exit_scene(self):
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
			self.add_scene(scene)
		#start the timer
		self.clock.tick(60)
		#encompass loop for easy exiting
		try:
			print("Scene Manager: Exiting game. Reason: {}.".format(self.main_loop()))
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

			#process events
			evt = self.event_handler()
			if(evt):
				return evt

			# ticks targetFPS times per second, divided by 1000 to convert ms to s
			delta = self.clock.tick(self.targetFPS) / 1000.0

			#protection against extremely low fps; pause if fps is below 
			if delta > (1.0 / self.minFPS):
				print("Scene Manager: Called scene ({}) pause() due to low FPS. Setting highest delta.".format(self.scenes[-1].get_name()))
				self.scenes[-1].pause()
				#set delta to highest allowed value for update protection
				delta = 1.0 / self.minFPS

			#only update and render current (top/focused) scene

			#try to update the current scene
			self.scenes[-1].update(delta)
			#right now this is the only leak, therefore it warrants a check here, but nowhere else.
			if not self.scenes: break

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

			
		return "no more scenes"
		#raise self.SafeExit("no more scenes")

	def event_handler(self):
		"""Handles events from pygame"""

		for evt in pygame.event.get():
			if  (evt.type == pygame.QUIT):            return "Window closed."
			elif(evt.type == pygame.MOUSEBUTTONUP):   return mouseManager.up_event(evt)
			elif(evt.type == pygame.MOUSEBUTTONDOWN): return mouseManager.down_event(evt)
			elif(evt.type == pygame.KEYDOWN):         return keyboardManager.down_event(evt)
			elif(evt.type == pygame.KEYUP):           return keyboardManager.up_event(evt)
			elif(evt.type == pygame.JOYAXISMOTION):   return gamepadManager.axis_motion_event(evt)
			elif(evt.type == pygame.JOYBALLMOTION):   return gamepadManager.ball_motion_event(evt)
			elif(evt.type == pygame.JOYHATMOTION):    return gamepadManager.hat_motion_event(evt)
			elif(evt.type == pygame.JOYBUTTONUP):     return gamepadManager.button_up_event(evt)
			elif(evt.type == pygame.JOYBUTTONDOWN):   return gamepadManager.button_down_event(evt)
			elif(evt.type == pygame.VIDEORESIZE):     return self.resize_event(evt)

	def resize_event(self, evt):
		"""Called when the screen is resized."""
		size = evt.size
		#Log this event. It's a dangerous one.
		print("Screen resized to: ({}, {}).".format(size[0], size[1]))
		#TEMPORARY STUFFS
		engine.graphics.resize(size)
		#engine.screen_bounds = engine.graphics.interface.screen_bounds
		#engine.window_scale = engine.graphics.interface.window_scale
		#engine.window_bounds = engine.graphics.interface.window_bounds
		#print(engine.graphics.interface.window_scale)
		#update the display window size
		pygame.display.set_mode(size, pygame.RESIZABLE )
		#update (replace) scene screens
		for i in range(len(self.screens)):
			#resize the screens
			self.screens[i] = pygame.Surface(gameScreen.get_size(),pygame.SRCALPHA)
			#re-render the resized scenes
			self.scenes[i].render(self.screens[i])


#Manages mouse events.
#Could use a few additional features, especially for buttons.
class MouseManager:

	def __init__(self):
		self.mouse_clicks = [[],[],[],[],[],[],[]]
		self.mouse_downs = [(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)]
		self.virtual_mode_enabled = False
		self.rel_movement = (0,0)

	def update(self):
		self.mouse_clicks = [[],[],[],[],[],[],[]]
		self.rel_movement = pygame.mouse.get_rel()
		if(self.virtual_mode_enabled):
			self.set_mouse_position((0,0))
			#setgameScreen.get_size() / 2

	def down_event(self, evt):
		self.mouse_downs[evt.button - 1] = evt.pos

	def up_event(self, evt):
		btn = evt.button - 1
		if(evt.pos == self.mouse_downs[btn]):
			self.mouse_clicks[btn].append(evt.pos)

	def get_clicks(self):
		"""Returns an array of arrays of tuples of mouse clicks since the last frame"""
		return self.mouse_clicks

	def get_mouse_position(self):
		"""Returns the current mouse position, as a tuple."""
		return pygame.mouse.get_pos()

	def set_mouse_position(self, pos):
		"""Sets the mouse position. Ideally, should only be used with setMouseGrab(True)."""
		return pygame.mouse.set_pos(pos[0], pos[1])

	def get_virtual_mode(self):
		"""Returns True if virtual mode is enabled."""
		if((pygame.event.get_grab() != self.virtual_mode_enabled) or (pygame.mouse.get_visible() != self.virtual_mode_enabled)):
			print("WARNING!: Invalid virtual mode state! Attempting to fix.")
			self.set_virtual_mode(self.virtual_mode_enabled)
		return pygame.event.get_grab()

	def get_mouse_movement(self):
		"""Gets relative mouse movement since last frame."""
		return self.rel_movement

	def set_virtual_mode(self, grb):
		"""Sets virtual mode (True or False)."""
		print("Virtual mode {}.".format("enabled" if grb else "disabled"))
		pygame.event.set_grab(grb)
		pygame.mouse.set_visible(not grb)
		return self.get_virtual_mode()

	def enter_virtual_mode(self):
		"""Enters virtual mode."""
		return self.set_virtual_mode(True)

	def leave_virtual_mode(self):
		"""Leaves virtual mode."""
		return self.set_virtual_mode(False)

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

	def down_event(self, evt):
		pass

	def up_event(self, evt):
		self.pressed[evt.key] = True

	def is_key_down(self, key):
		"""Returns True if key is currently being pressed."""
		return self.state[key]

	def was_key_pressed(self, key):
		"""Returns True if the key was pressed last frame."""
		return self.pressed[key]

#Manages gamepad events.
#Not yet implemented.
#use pygame.joystick, and ignore trackball stuff for now
class GamepadManager:

	def __init__(self):
		pass

	def update(self):
		pass

	def axis_motion_event(self, evt):
		pass

	def ball_motion_event(self, evt):
		pass

	def hat_motion_event(self, evt):
		pass

	def button_up_event(self, evt):
		pass

	def button_down_event(self, evt):
		pass

mouseManager = MouseManager()
keyboardManager = KeyboardManager()
gamepadManager = GamepadManager()
sceneManager = SceneManager()
