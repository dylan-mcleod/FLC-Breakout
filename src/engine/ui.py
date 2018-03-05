import engine
import pygame



class FontSizer:
	
	def __init__(self, font_name):
		self.font_name = font_name
		self.sizes = {}
	
	def get_size(self, size):
		font = self.sizes.get(size)
		if not font:
			font = engine.get_font(self.font_name, size)
			self.sizes[size] = font
		return font


GAME_FONT = FontSizer("Regular")
GAME_FONT_BOLD = FontSizer("Bold")

GAME_FONT_COLOR          = (255, 255, 255)
GAME_FONT_COLOR_ACTIVE   = (185, 185, 185)
GAME_FONT_COLOR_DISABLED = (100, 100, 100)

GAME_MENU_BG_COLOR       = (0,   0,   0,  150)

DEFAULT_MENU_PADDING     = .05
DEFAULT_FONT_HEIGHT      = .1


def initialize_ui():
	engine.load_font("Regular", "Orbitron-Regular")
	engine.load_font("Bold", "Orbitron-Bold")



class UIElement:
	
	def __init__(self, width = 0, height = 0):
		self.bounds = engine.SRect(0, 0, width, height)
		self.offset = (0, 0)
		self.anchor = engine.Anchor.CENTER
		self.parent = None
		self._update_bounds_position()
	
	
	def _get_parent_bounds(self):
		if self.parent:
			return self.parent.bounds
		else:
			return engine.get_screen_bounds()
	
	
	def _update_bounds_position(self):
		ox, oy = self.offset
		px, py = self._get_parent_bounds().get_pos(self.anchor)
		self.bounds.set_pos((px + ox, py + oy), self.anchor)
		# Extensions extend this
	
	
	# UIGroup sets offsets and anchors of children directly, 
	# doesn't use these methods
	
	def set_offset(self, offset):
		if type(self.parent) is not UIGroup:
			self.offset = offset
			self._update_bounds_position()
	
	
	def set_anchor(self, anchor):
		if type(self.parent) is not UIGroup:
			self.anchor = anchor
			self._update_bounds_position()
	
	
	def draw(self, destination_surface):
		pass
		# Extensions override this




class UIParent(UIElement):

	def __init__(self, width = 0, height = 0):
		self.children = []
		self.background_color = None
		self.background_surface = None
		super().__init__(width, height)
	
	
	def _update_bounds_position(self):
		super()._update_bounds_position()
		for child in self.children:
			child._update_bounds_position()
	
	
	def _add_child(self, child):
		self.children.append(child)
		child.parent = self
	
	
	def _create_background(self, rect):
		self.background_surface = pygame.Surface(rect.size, flags = pygame.SRCALPHA)
		self.background_surface.fill(self.background_color)
	
	
	def set_background(self, background_color = GAME_MENU_BG_COLOR):
		self.background_color = background_color
		if background_color:
			self._create_background(self.bounds.toRect())
	
	
	def draw(self, destination_surface):
		if self.background_color:
			bounds_rect = self.bounds.toRect()
			bg_rect = self.background_surface.get_rect()
			if(bg_rect.size != bounds_rect.size):
				self._create_background(bounds_rect)
			destination_surface.blit(self.background_surface, bounds_rect)
		
		for child in self.children:
			child.draw(destination_surface)




class UIFrame(UIParent):
	
	def resize(self, size):
		self.bounds.size = size
		self._update_bounds_position()
	
	
	def add_child(self, child):
		if child.parent:
			return
		self._add_child(child)
		child._update_bounds_position()





def get_group_child_anchor(menu_anchor):
	return engine.Anchor(int(menu_anchor) % 3)


def get_first_group_child_offset(anchor, bounds, p):
	return ([p, 0, -p][int(anchor)], p)



class UIGroup(UIParent):
	
	def __init__(self, padding = DEFAULT_MENU_PADDING):
		super().__init__()
		self.padding = padding
	
	
	def _arrange_children(self):
		w = 0
		h = 0
		for child in self.children:
			if child.bounds.width > w:
				w = child.bounds.width
			h += child.bounds.height
		
		p = self.padding*2
		self.bounds.size = (w + p, h + p)
		UIElement._update_bounds_position(self)
		
		child_anchor = get_group_child_anchor(self.anchor)
		x, y = get_first_group_child_offset(child_anchor, self.bounds, self.padding)
		for child in self.children:
			child.offset = (x, y)
			child.anchor = child_anchor
			child._update_bounds_position()
			y += child.bounds.height
	
	
	def add_child(self, child):
		if child.parent or type(child) is UIGroup:
			return
		self._add_child(child)
		self._arrange_children()





class TextElement:
	
	def __init__(self, text_string, font, color):
		self.surface = font.render(text_string, True, color)
	
	
	def get_engine_width(self, height):
		rect = self.surface.get_rect()
		return height*(rect.width/rect.height)
	
	def draw(self, destination_surface, bounds):
		destination_surface.blit(self.surface, bounds.toRect())





class Text_Base:
	
	# returns engine width
	def _set_font_size(self, font_size):
		self.font_size = font_size
		# pygame seems to have an off-by-one error     VVV
		self.font = self.font_sizer.get_size(font_size - 1)
		return self._render()
	
	
	# returns engine width
	def _init(self, text_string, height, font):
		self.text_string = text_string
		self.height = height
		self.font_sizer = font
		return self._set_font_size(engine.to_pygame_units(height))
	
	
	def set_string(self, text_string):
		self.text_string = text_string
		self.bounds.width = self._render()
		if type(self.parent) is UIGroup:
			self.parent._arrange_children()
		else:
			self._update_bounds_position()
	
	
	def _update_font_size(self):
		font_size = engine.to_pygame_units(self.height)
		if font_size != self.font_size:
			self._set_font_size(font_size)





class UIText(UIElement, Text_Base):
	
	def _render(self):
		self.text = TextElement(self.text_string, self.font, self.color)
		return self.text.get_engine_width(self.height)
	
	
	def __init__(self, text_string, height = DEFAULT_FONT_HEIGHT, 
	             font = GAME_FONT, color = GAME_FONT_COLOR):
		self.color = color
		super().__init__(self._init(text_string, height, font), height)
	
	
	def set_color(self, color):
		self.color = color
		self._render()
	
	
	def draw(self, destination_surface):
		self._update_font_size()
		self.text.draw(destination_surface, self.bounds)



# class UI_Image(UIElement)



class UIMenuItem(UIElement):
	
	def __init__(self, width = 0, height = 0):
		super().__init__(width, height)
		self.is_active = False
		self.is_enabled = True
		self.was_selected = False
	
	
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




class UITextButton(UIMenuItem, Text_Base):
	
	def _render(self):
		self.inactive_text = TextElement(self.text_string, self.font, GAME_FONT_COLOR)
		self.active_text = TextElement(self.text_string, self.font, GAME_FONT_COLOR_ACTIVE)
		self.disabled_text = TextElement(self.text_string, self.font, GAME_FONT_COLOR_DISABLED)
		return self.inactive_text.get_engine_width(self.height)
	
	
	def __init__(self, text_string, height = DEFAULT_FONT_HEIGHT, font = GAME_FONT):
		super().__init__(self._init(text_string, height, font), height)
	
	
	def draw(self, destination_surface):
		self._update_font_size()
		if not self.is_enabled:
			self.disabled_text.draw(destination_surface, self.bounds)
		elif self.is_active:
			self.active_text.draw(destination_surface, self.bounds)
		else:
			self.inactive_text.draw(destination_surface, self.bounds)



# class UI_Image_Button(UIMenuItem)
# class UI_Slider(UIMenuItem)




class UIMenu:
	
	def __init__(self):
		self.items = []
		self.active = 0
		self.selected = -1
		self.mouse_overlapped = False
	
	
	def add_item(self, item):
		self.items.append(item)
		if len(self.items) == 1:
			item.set_active(True)
	
	
	def _change_active(self, n):
		self.items[self.active].set_active(False)
		self.active = (self.active + n) % len(self.items)
		self.items[self.active].set_active(True)
	
	
	def update(self):
		if self.selected != -1:
			self.items[self.selected].was_selected = False
			self.selected = -1
		
		mouse_position = engine.get_mouse_position()
		mouse_overlapped = False
		for i, item in enumerate(self.items):
			if item.bounds.toRect().collidepoint(mouse_position):
				mouse_overlapped = True
				if not item.is_active:
					self.items[self.active].set_active(False)
					item.set_active(True)
					self.active = i
					break
		
		if not mouse_overlapped:
			if engine.was_key_pressed(pygame.K_UP):
				self._change_active(-1)
			elif engine.was_key_pressed(pygame.K_DOWN):
				self._change_active(1)
		
		ai = self.items[self.active]
		ai.update()
		if ai.is_enabled:
			left_mouse_clicked = len(engine.get_clicks()[0])
			if engine.was_key_pressed(pygame.K_RETURN) or \
			   (left_mouse_clicked and mouse_overlapped):
				self.selected = self.active
				ai.was_selected = True
