import pygame
import engine
import scenes

class DummySetting(engine.UITextButton):
	
	def _get_dummy_text(self):
		return "Dummy setting: " + ["low", "medium", "high"][self.n]
	
	def dummy_select(self):
		self.n = (self.n + 1) % 3
		self.set_string(self._get_dummy_text())
	
	def __init__(self):
		self.n = 0
		super().__init__(self._get_dummy_text())

class SettingsScene(engine.Scene):

	def __init__(self):
		self.frame = engine.UIFrame(1.5, 1.75)
		self.frame.set_background()
		group = engine.UIGroup()
		self.frame.add_child(group)
		group.set_anchor(engine.Anchor.TOP_LEFT)
		self.menu = engine.UIMenu()
		group.add_child(engine.UIText("Settings:", .15, engine.GAME_FONT_BOLD))
		
		self.dummy_a = DummySetting()
		group.add_child(self.dummy_a)
		self.menu.add_item(self.dummy_a)
		
		self.dummy_b = DummySetting()
		group.add_child(self.dummy_b)
		self.menu.add_item(self.dummy_b)
		self.dummy_b.set_enabled(False)
		
		self.dummy_c = DummySetting()
		group.add_child(self.dummy_c)
		self.menu.add_item(self.dummy_c)
		
		self.back_button = engine.UITextButton("Back")
		self.frame.add_child(self.back_button)
		self.menu.add_item(self.back_button)
		self.back_button.set_anchor(engine.Anchor.BOTTOM_RIGHT)
		self.back_button.set_offset((-engine.DEFAULT_MENU_PADDING, -engine.DEFAULT_MENU_PADDING))


	def update(self, delta):
		self.menu.update()
		if self.dummy_a.was_selected:
			self.dummy_a.dummy_select()
		elif self.dummy_b.was_selected:
			self.dummy_b.dummy_select()
		elif self.dummy_c.was_selected:
			self.dummy_c.dummy_select()
		elif self.back_button.was_selected:
			engine.switch_scene(scenes.TitleScene())


	def render(self, surface):
		surface.fill((150, 150, 150, 255))
		self.frame.draw(surface)


	def pause(self):
		pass
