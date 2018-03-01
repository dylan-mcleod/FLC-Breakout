import pygame
import engine
import scenes
import pygame.font

class MainMenuScene(engine.Scene):

	def __init__(self):
		self.menu = engine.Menu(anchor = engine.Anchor.BOTTOM_RIGHT, header_string = "Breakout")
		
		play_item = self.menu.add_item()
		play_item.set_contents("Play")
		
		settings_item = self.menu.add_item()
		settings_item.set_contents("Settings")
		settings_item.set_grayed(True)
		self.settings_item = settings_item
		
		quit_item = self.menu.add_item()
		quit_item.set_contents("Quit")


	def update(self, delta):
		#for now, just go straight to the play scene on any left click or enter
		if engine.getClicks()[0] or engine.wasKeyPressed(pygame.K_RETURN): engine.switchScene(scenes.PlayScene())
		# when G key is pressed, toggle grayness of settings menu item
		if engine.wasKeyPressed(pygame.K_g):
			self.settings_item.set_grayed(not self.settings_item.is_grayed)


	def render(self, surface):
		surface.fill((0, 0, 0, 255))
		width, height = surface.get_size()
		self.menu.set_position((width/2, height/2))
		self.menu.draw(surface)


	def pause(self):
		pass
