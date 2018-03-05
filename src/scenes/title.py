import pygame
import engine
import scenes

class TitleScene(engine.Scene):

	def __init__(self):
		self.title = engine.UIText("Breakout!", .3, engine.GAME_FONT_BOLD)
		self.title.set_offset((0, -.2))
		
		self.menu_group = engine.UIGroup()
		self.menu_group.set_anchor(engine.Anchor.BOTTOM_RIGHT)
		self.menu_group.set_offset((-.1, -.1))
		self.menu_group.set_background()
		self.menu = engine.UIMenu()
		
		self.play_button = engine.UITextButton("Play")
		self.menu_group.add_child(self.play_button)
		self.menu.add_item(self.play_button)
		
		self.settings_button = engine.UITextButton("Settings")
		self.menu_group.add_child(self.settings_button)
		self.menu.add_item(self.settings_button)
		
		self.credits_button = engine.UITextButton("Credits")
		self.menu_group.add_child(self.credits_button)
		self.menu.add_item(self.credits_button)
		
		self.quit_button = engine.UITextButton("Quit")
		self.menu_group.add_child(self.quit_button)
		self.menu.add_item(self.quit_button)


	def update(self, delta):
		self.menu.update()
		if self.play_button.was_selected:
			engine.switch_scene(scenes.PlayScene())
		elif self.settings_button.was_selected:
			engine.switch_scene(scenes.SettingsScene())
		elif self.credits_button.was_selected:
			engine.switch_scene(scenes.CreditsScene())
		elif self.quit_button.was_selected:
			engine.exit_scene()


	def render(self, surface):
		surface.blit(engine.get_image("metal background"), pygame.Rect(0,0,1920,1080))
		self.menu_group.draw(surface)
		self.title.draw(surface)


	def pause(self):
		pass



