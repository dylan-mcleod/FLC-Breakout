import engine
import pygame



class Font_Sizer:
	
	def __init__(self, font_name):
		self.font_name = font_name
		self.sizes = {}
	
	def get_size(self, size):
		font = self.sizes.get(size)
		if not font:
			font = engine.get_font(self.font_name, size)
			self.sizes[size] = font
		return font


GAME_FONT = Font_Sizer("Regular")
GAME_FONT_BOLD = Font_Sizer("Bold")

GAME_FONT_COLOR        = (255, 255, 255)
GAME_FONT_COLOR_ACTIVE = (200, 200, 200)
GAME_FONT_COLOR_GRAYED = (100, 100, 100)

GAME_MENU_BG_COLOR     = (0,   0,   0,  150)

DEFAULT_MENU_PADDING   = .05
DEFAULT_FONT_HEIGHT    = .1


def initialize_ui():
	engine.load_font("Regular", "Orbitron-Regular")
	engine.load_font("Bold", "Orbitron-Bold")



class UI_Element:
	
	def __init__(self, width = 0, height = 0):
		self.bounds = engine.SRect(0, 0, width, height)
		self.offset = (0, 0)
		self.anchor = engine.Anchor.CENTER
		self.parent = None
		self.background_color = None
		self.background_surface = None
	
	
	def _get_parent_bounds(self):
		if self.parent:
			return self.parent.bounds
		else:
			return engine.screen_bounds
	
	
	def _update_bounds_position(self):
		ox, oy = self.offset
		px, py = self._get_parent_bounds().get_pos(self.anchor)
		self.bounds.set_pos((px + ox, py + oy), self.anchor)
		# Extensions extend this
	
	def _create_background(self, rect):
		self.background_surface = pygame.Surface(rect.size, flags = pygame.SRCALPHA)
		self.background_surface.fill(self.background_color)
	
	def set_background(self, background_color = GAME_MENU_BG_COLOR):
		self.background_color = background_color
		if background_color:
			self._create_background(self.bounds.toRect())
	
	
	# UI_Group sets offsets and anchors of children directly, 
	# doesn't use these methods
	
	def set_offset(self, offset):
		if type(self.parent) is not UI_Group:
			self.offset = offset
			self._update_bounds_position()
	
	
	def set_anchor(self, anchor):
		if type(self.parent) is not UI_Group:
			self.anchor = anchor
			self._update_bounds_position()
	
	
	def draw(self, destination_surface):
		if self.background_color:
			bounds_rect = self.bounds.toRect()
			bg_rect = self.background_surface.get_rect()
			if(bg_rect.size != bounds_rect.size):
				self._create_background(bounds_rect)
			destination_surface.blit(self.background_surface, bounds_rect)
		# Extensions extend this





class UI_Frame(UI_Element):
	
	def __init__(self, width, height):
		super().__init__(width, height)
		children = []
	
	
	def _update_bounds_position(self):
		super()._update_bounds_position()
		for child in self.children:
			child._update_bounds_position()
	
	
	def resize(self, size):
		self.bounds.size = size
		self._update_bounds_position()
	
	
	def add_child(self, child):
		if child.parent:
			return
		self.children.append(child)
		child.parent = self
		child._update_bounds_position()
	
	
	def draw(self, destination_surface):
		super().draw(destination_surface)
		for child in self.children:
			child.draw(destination_surface)





def get_group_child_anchor(menu_anchor):
	return engine.Anchor(int(menu_anchor) % 3)


def get_first_group_child_offset(anchor, bounds, p):
	return ([p, 0, -p][int(anchor)], p)



class UI_Group(UI_Element):
	
	def __init__(self, padding = DEFAULT_MENU_PADDING):
		super().__init__()
		self.children = []
		self.padding = padding
	
	
	def _update_bounds_position(self):
		super()._update_bounds_position()
		for child in self.children:
			child._update_bounds_position()
	
	
	def _arrange_children(self):
		w = 0
		h = 0
		for child in self.children:
			if child.bounds.width > w:
				w = child.bounds.width
			h += child.bounds.height
		
		p = self.padding*2
		self.bounds.size = (w + p, h + p)
		super()._update_bounds_position()
		
		child_anchor = get_group_child_anchor(self.anchor)
		x, y = get_first_group_child_offset(child_anchor, self.bounds, self.padding)
		for child in self.children:
			child.offset = (x, y)
			child.anchor = child_anchor
			child._update_bounds_position()
			y += child.bounds.height
	
	
	def add_child(self, child):
		if child.parent or type(child) is UI_Group:
			return
		self.children.append(child)
		child.parent = self
		self._arrange_children()
	
	
	def draw(self, destination_surface):
		super().draw(destination_surface)
		for child in self.children:
			child.draw(destination_surface)





class UI_Text(UI_Element):
	
	# TODO: can I reuse code between this and UI_Text_Button?
	
	# returns engine width
	def _render(self):
		self.surface = self.font.render(self.text_string, True, self.color)
		rect = self.surface.get_rect()
		return self.height*(rect.width/rect.height)
	
	
	# returns engine width
	def _set_font_size(self, font_size):
		self.font_size = font_size
		# pygame seems to have an off-by-one error     VVV
		self.font = self.font_sizer.get_size(font_size - 1) 
		return self._render()
	
	
	def __init__(self, text_string, height = DEFAULT_FONT_HEIGHT, 
	             font = GAME_FONT, color = GAME_FONT_COLOR):
		self.text_string = text_string
		self.height = height
		self.color = color
		self.font_sizer = font
		super().__init__(self._set_font_size(engine.to_pygame_units(height)), height)
	
	
	def set_string(self, text_string):
		self.text_string = text_string
		self.bounds.width = self._render()
		if type(self.parent) is UI_Group:
			self.parent._arrange_children()
		else:
			self._update_bounds_position()
	
	
	def draw(self, destination_surface):
		super().draw(destination_surface)
		font_size = engine.to_pygame_units(self.height)
		if font_size != self.font_size:
			self._set_font_size(font_size)
		destination_surface.blit(self.surface, self.bounds.toRect())


# class UI_Image(UI_Element)



class UI_Menu_Item(UI_Element):
	
	def __init__(self, width = 0, height = 0):
		super().__init__(width, height)
		self.is_active = False
		self.is_enabled = True
	
	
	def set_active(self, is_active):
		self.is_active = is_active
		# Extensions override this
	
	
	def set_enabled(self, is_enabled):
		self.is_enabled = is_enabled
		# Extensions override this
	
	
	def update(self):
		pass
		# Extensions override this
		# Planning on using this for things like sliders
	
	
	def execute(self):
		pass
		# Extensions override this




class UI_Text_Button(UI_Menu_Item):
	
	def __init__(self, text_string, height, font):
		# TODO
		pass
	
	
	def set_string(self, text_string):
		# TODO
		pass
	
	
	def set_enabled(self, is_enabled):
		# TODO
		pass
	
	
	def draw(self, destination_surface):
		# TODO
		pass



# class UI_Image_Button(UI_Menu_Item)
# class UI_Slider(UI_Menu_Item)




class UI_Menu:
	
	def __init__(self):
		self.items = []
		self.active = -1
	
	
	def add_item(self, item):
		self.items.append(item)
	
	
	def update(self):
		# TODO
		pass
