import pygame
import engine
import scenes

class Dummy_Setting(engine.UI_Text_Button):
	
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
		self.frame = engine.UI_Frame(1.5, 1.75)
		self.frame.set_background()
		group = engine.UI_Group()
		self.frame.add_child(group)
		group.set_anchor(engine.Anchor.TOP_LEFT)
		self.menu = engine.UI_Menu()
		group.add_child(engine.UI_Text("Settings:", .15, engine.GAME_FONT_BOLD))
		
		self.dummy_a = Dummy_Setting()
		group.add_child(self.dummy_a)
		self.menu.add_item(self.dummy_a)
		
		self.dummy_b = Dummy_Setting()
		group.add_child(self.dummy_b)
		self.menu.add_item(self.dummy_b)
		self.dummy_b.set_enabled(False)
		
		self.dummy_c = Dummy_Setting()
		group.add_child(self.dummy_c)
		self.menu.add_item(self.dummy_c)
		
		self.back_button = engine.UI_Text_Button("Back")
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
			engine.switchScene(scenes.MainMenuScene())


	def render(self, surface):
		surface.fill((150, 150, 150, 255))
		self.frame.draw(surface)


	def pause(self):
		pass
