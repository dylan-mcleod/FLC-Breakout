import pygame
import engine
import scenes

class CreditsScene(engine.Scene):

	def __init__(self):
		self.credits_frame = engine.UIFrame(1.5, 1.5)
		group = engine.UIGroup()
		self.credits_frame.add_child(group)
		group.set_anchor(engine.Anchor.TOP_LEFT)
		
		group.add_child(engine.UIText("Dylan McLeod", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UIText("Michael Grant", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UIText("Sean Tedrow", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UIText("Shareen Abdul", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UIText("Jaseem Nazeer", font = engine.GAME_FONT_BOLD))
		group.add_child(engine.UIText("Cash Rion", font = engine.GAME_FONT_BOLD))
		
		self.back_button = engine.UITextButton("Back")
		self.back_button.set_anchor(engine.Anchor.BOTTOM_RIGHT)
		self.back_button.set_offset((-engine.DEFAULT_MENU_PADDING, -engine.DEFAULT_MENU_PADDING))
		self.credits_frame.add_child(self.back_button)
		self.menu = engine.UIMenu()
		self.menu.add_item(self.back_button)

	def update(self, delta):
		self.menu.update()
		if self.back_button.was_selected:
			engine.switch_scene(scenes.TitleScene())


	def render(self, surface):
		surface.fill((150, 150, 150, 255))
		self.credits_frame.draw(surface)
		self.back_button.draw(surface)


	def pause(self):
		pass
