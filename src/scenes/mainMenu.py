import pygame
import engine
import scenes

class MainMenuScene(engine.Scene):

	def __init__(self):
		self.title = engine.UI_Text("Breakout!", .3, engine.GAME_FONT_BOLD)
		self.title.set_offset((0, -.2))
		
		self.menu_group = engine.UI_Group()
		self.menu_group.set_anchor(engine.Anchor.BOTTOM_RIGHT)
		self.menu_group.set_offset((-.1, -.1))
		self.menu_group.set_background()
		
		self.menu_group.add_child(engine.UI_Text("Play"))
		self.menu_group.add_child(engine.UI_Text("Settings"))
		self.menu_group.add_child(engine.UI_Text("Credits"))
		self.menu_group.add_child(engine.UI_Text("Quit"))


	def update(self, delta):
		#for now, just go straight to the play scene on any left click or enter
		if engine.getClicks()[0] or engine.wasKeyPressed(pygame.K_RETURN): engine.switchScene(scenes.PlayScene())


	def render(self, surface):
		surface.fill((150, 150, 150, 255))
		self.menu_group.draw(surface)
		self.title.draw(surface)


	def pause(self):
		pass
