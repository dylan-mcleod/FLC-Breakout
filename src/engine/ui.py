import pygame
import engine
from engine.scaling import *
import os
# TODO: input and paths

class Font_Fetcher:
	
	def __init__(self, path):
		self.path = path
		self.sizes = {}
	
	def get_size(self, size):
		font = self.sizes.get(size)
		if not font:
			font = pygame.font.Font(self.path, int(window_scale*size))
			self.sizes[size] = font
		return font

# TODO: paths, think I need asset acquisition module
GAME_FONT_PATH = os.path.abspath("..\\assets\\fonts\\Orbitron-Bold.ttf")
GAME_FONT_BOLD_PATH = os.path.abspath("..\\assets\\fonts\\Orbitron-Black.ttf")

GAME_FONT = Font_Fetcher(GAME_FONT_PATH)
GAME_FONT_BOLD = Font_Fetcher(GAME_FONT_BOLD_PATH)

GAME_FONT_COLOR        = (255, 255, 255)
GAME_FONT_COLOR_ACTIVE = (200, 200, 200)
GAME_FONT_COLOR_GRAYED = (100, 100, 100)


class Location:
	
	def __init__(self, position = (0, 0), anchor = Anchor.TOP_LEFT):
		self.position = position
		self.anchor = anchor

def set_rect_location(rect, location):
	rect.set_pos(location.position, location.anchor)

#class UIGroup
#class UIElement(UIGroup)
#TextButton(UIElement)
#Image(UIElement)
#Imagebutton(UIElement)


class Text:
	
	def __init__(self):
		self.surface = None
		self.bounds = engine.SRect(0, 0, 0, 0)
		self.location = Location()
	
	def render_with_font(self, text_string, font, color):
		self.surface = font.render(text_string, True, color)
		self.bounds = engine.SRect.fromRect(self.surface.get_rect())
		set_rect_location(self.bounds, self.location)
	
	def render(self, text_string, size, color = GAME_FONT_COLOR):
		self.render_with_font(text_string, GAME_FONT.get_size(size), color)
		
	def set_anchor(self, anchor):
		self.location.anchor = anchor
		set_rect_location(self.bounds, self.location)
	
	def set_position(self, position):
		self.location.position = position
		set_rect_location(self.bounds, self.location)
	
	def set_location(self, location):
		self.location = location
		set_rect_location(self.bounds, self.location)
	
	def draw(self, dest_surface):
		if self.surface:
			dest_surface.blit(self.surface, self.bounds.toRect())



class Menu_Item:
	
	def __init__(self, parent_menu, callback, data):
		self.contents = ""
		self.text = Text()
		self.parent_menu = parent_menu
		self.is_active = False;
		self.is_grayed = False;
		self.callback = callback
		self.data = data
	
	def get_color(self):
		if self.is_grayed:
			return GAME_FONT_COLOR_GRAYED
		elif self.is_active:
			return GAME_FONT_COLOR_ACTIVE
		else:
			return GAME_FONT_COLOR
	
	def render_text(self):
		font = self.parent_menu.item_font
		self.text.render_with_font(self.contents, font, self.get_color())
	
	def set_contents(self, contents):
		self.contents = contents
		self.render_text()
		self.parent_menu.has_been_resized = True
	
	def set_grayed(self, to_gray):
		self.is_grayed = to_gray
		self.render_text()
	
	def set_active(self, to_active):
		self.is_active = to_active
		self.render_text()



def get_menu_item_anchor(menu_anchor):
	return engine.Anchor(int(menu_anchor) % 3)

def get_menu_item_x(anchor, width):
	return [0, width/2, width][int(anchor)]

class Menu:
	
	def __init__(self, anchor = Anchor.TOP_LEFT, item_size = 0.18, 
	             header_string = None, header_size = 0.22):
		self.item_font = GAME_FONT.get_size(item_size)
		self.location = Location((0, 0), anchor)
		self.items = []
		self.active_item_index = -1
		self.surface = None
		self.bounds = engine.SRect(0, 0, 0, 0)
		
		if header_string:
			header = Text()
			header.set_anchor(get_menu_item_anchor(anchor))
			header_font = GAME_FONT_BOLD.get_size(header_size)
			header.render_with_font(header_string, header_font, GAME_FONT_COLOR)
			
			self.header_text = header
			self.header_size = header.bounds.size
			self.has_been_resized = True
		else:
			self.header_text = None
			self.header_size = (0, 0)
			self.has_been_resized = False
	
	
	def add_item(self, callback = None, data = None):
		item = Menu_Item(self, callback, data)
		item.text.set_anchor(get_menu_item_anchor(self.location.anchor))
		self.items.append(item)
		self.has_been_resized = True
		return item
	
	
	def set_position(self, position):
		self.location.position = position
		set_rect_location(self.bounds, self.location)
	
	
	def create_surface(self, width, height):
		self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
	
	def handle_resize(self):
		width, height = self.header_size
		y = height
		height += (self.item_font.get_height() * len(self.items))
		for item in self.items:
			item_width = item.text.bounds.width
			if item_width > width:
				width = item_width
		x = get_menu_item_x(get_menu_item_anchor(self.location.anchor), width)
		item_height = self.item_font.get_height()
		
		if self.header_text:
			self.header_text.set_position((x, 0))
		for item in self.items:
			item.text.set_position((x, y))
			y += item_height
		
		if not self.surface:
			self.create_surface(width, height)
		elif width > self.surface.get_width() or height > self.surface.get_height():
			self.create_surface(width, height)
		self.bounds.size = (width, height)
		set_rect_location(self.bounds, self.location)
	
	
	def draw(self, dest_surface):
		if self.has_been_resized and (self.header_text or self.items):
			self.handle_resize()
			self.has_been_resized = False
		elif not self.surface:
			return
		self.surface.fill((0, 0, 0, 0), special_flags = pygame.BLEND_RGBA_MIN)
		if self.header_text:
			self.header_text.draw(self.surface)
		for item in self.items:
			item.text.draw(self.surface)
		dest_surface.blit(self.surface, self.bounds.toRect())
	
	
	def update(self, passthrough = None):
		# TODO
		# IMPORTANT NOTE: callbacks receive item and passthrough.
		pass


