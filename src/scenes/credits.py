import pygame
import engine
import scenes

class CreditsScene(engine.Scene):

	def __init__(self):
		self.credits_frame = engine.UI_Frame(1.5, 1.5)
		group = engine.UI_Group()
		self.credits_frame.add_child(group)
		group.set_anchor(engine.Anchor.TOP_LEFT)
		
		group.add_child(engine.UI_Text("Dylan McLeod", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UI_Text("Michael Grant", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UI_Text("Sean Tedrow", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UI_Text("Shareen Abdul", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UI_Text("Jaseem Nazeer", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UI_Text("Cash Rion", font = engine.GAME_FONT_BOLD))
		
		self.back_button = engine.UI_Text_Button("Back")
		self.back_button.set_anchor(engine.Anchor.BOTTOM_RIGHT)
		self.back_button.set_offset((-.1, -.1))
		self.menu = engine.UI_Menu()
		self.menu.add_item(self.back_button)

	def update(self, delta):
		self.menu.update()
		if self.back_button.was_selected:
			engine.switchScene(scenes.MainMenuScene())


	def render(self, surface):
		surface.fill((150, 150, 150, 255))
		self.credits_frame.draw(surface)
		self.back_button.draw(surface)


	def pause(self):
		pass
