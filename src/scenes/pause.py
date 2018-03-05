import pygame
import engine
import scenes

class PauseScene(engine.Scene):

	def __init__(self):
		self.group = engine.UIGroup()
		self.group.set_background()
		self.group.add_child(engine.UIText("Paused", .15, engine.GAME_FONT_BOLD))
		self.menu = engine.UIMenu()
		
		self.resume_button = engine.UITextButton("Resume")
		self.group.add_child(self.resume_button)
		self.menu.add_item(self.resume_button)
		
		self.main_menu_button = engine.UITextButton("Return to main menu")
		self.group.add_child(self.main_menu_button)
		self.menu.add_item(self.main_menu_button)


	def update(self, delta):
		self.menu.update()
		if self.resume_button.was_selected or engine.was_key_pressed(pygame.K_ESCAPE):
			engine.exit_scene()
		elif self.main_menu_button.was_selected:
			engine.replace_scene(scenes.TitleScene())



	def render(self, surface):
		surface.fill((0, 0, 0, 0), special_flags = pygame.BLEND_RGBA_MIN)
		self.group.draw(surface)


	def pause(self):
		pass
