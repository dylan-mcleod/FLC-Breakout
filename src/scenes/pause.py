import pygame
import engine
import scenes

class PauseScene(engine.Scene):

	def __init__(self):
		self.group = engine.UI_Group()
		self.group.set_background()
		self.group.add_child(engine.UI_Text("Paused", .15, engine.GAME_FONT_BOLD))
		self.menu = engine.UI_Menu()
		
		self.resume_button = engine.UI_Text_Button("Resume")
		self.group.add_child(self.resume_button)
		self.menu.add_item(self.resume_button)
		
		self.main_menu_button = engine.UI_Text_Button("Return to main menu")
		self.group.add_child(self.main_menu_button)
		self.menu.add_item(self.main_menu_button)


	def update(self, delta):
		self.menu.update()
		if self.resume_button.was_selected or engine.wasKeyPressed(pygame.K_ESCAPE):
			engine.exitScene()
		elif self.main_menu_button.was_selected:
			engine.replaceScene(scenes.MainMenuScene())



	def render(self, surface):
		surface.fill((0, 0, 0, 0), special_flags = pygame.BLEND_RGBA_MIN)
		self.group.draw(surface)


	def pause(self):
		pass
