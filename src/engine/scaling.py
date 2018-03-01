import pygame
from enum import Enum

#Le Anchor enum, created by Tau
class Anchor(Enum):
	TOP_LEFT      = 0
	TOP_CENTER    = 1
	TOP_RIGHT     = 2
	CENTER_LEFT   = 3
	CENTER        = 4
	CENTER_RIGHT  = 5
	BOTTOM_LEFT   = 6
	BOTTOM_CENTER = 7
	BOTTOM_RIGHT  = 8

	def __int__(self):
		return self.value

#Behold the scaled rect!
#A floating point python implementation of pygame.Rect, with some extra funtionality.
#Supremely useful for everything but direct rendering.
#TODO: Implement remaining methods provided by pygame.Rect
class SRect:

	def __init__(self, x, y, w, h):
		self.__x = x
		self.__y = y
		self.__w = w
		self.__h = h

	@classmethod
	def copy(self, srect):
		self.__x = srect.__x
		self.__y = srect.__y
		self.__w = srect.__w
		self.__h = srect.__h

	@classmethod
	def fromCoords(self, xy, wh):
		(self.__x, self.__y) = xy
		(self.__w, self.__h) = wh

	@classmethod
	def fromRect(cls, rct):
		return cls(rct.x, rct.y, rct.w, rct.h)

	def __str__(self):
		return "{}, {}, {}, {}".format(self.__x, self.__y, self.__w, self.__h)

	def set_pos(self, point, anchor = Anchor.CENTER):
		if  (anchor == Anchor.TOP_LEFT)     : self.topleft = point
		elif(anchor == Anchor.TOP_CENTER)   : self.midtop = point
		elif(anchor == Anchor.TOP_RIGHT)    : self.topright = point
		elif(anchor == Anchor.CENTER_LEFT)  : self.midleft = point
		elif(anchor == Anchor.CENTER)       : self.center = point
		elif(anchor == Anchor.CENTER_RIGHT) : self.midright = point
		elif(anchor == Anchor.BOTTOM_LEFT)  : self.bottomleft = point
		elif(anchor == Anchor.BOTTOM_CENTER): self.midbottom = point
		elif(anchor == Anchor.BOTTOM_RIGHT) : self.bottomright = point

	def get_pos(self, point, anchor = Anchor.CENTER):
		return {
			Anchor.TOP_LEFT      : self.topleft,
			Anchor.TOP_CENTER    : self.midtop,
			Anchor.TOP_RIGHT     : self.topright,
			Anchor.CENTER_LEFT   : self.midleft,
			Anchor.CENTER        : self.center,
			Anchor.CENTER_RIGHT  : self.midright,
			Anchor.BOTTOM_LEFT   : self.bottomleft,
			Anchor.BOTTOM_CENTER : self.midbottom,
			Anchor.BOTTOM_RIGHT  : self.bottomright
		}.get(anchor, self.topleft)

	def moveBy(self, delta):
		(self.__x, self.__y) = (self.__x + delta[0], self.__y + delta[1])

	def toRect(self):
		return pygame.Rect(self.__x, self.__y, self.__w, self.__h)

	#x
	@property
	def x(self):
		return self.__x

	@x.setter
	def x(self, x):
		self.__x = x

	#y
	@property
	def y(self):
		return self.__y

	@y.setter
	def y(self, y):
		self.__y = y

	#w
	@property
	def w(self):
		return self.__w

	@w.setter
	def w(self, w):
		self.__w = w

	#h
	@property
	def h(self):
		return self.__h

	@h.setter
	def h(self, h):
		self.__ch = h

	#size
	@property
	def size(self):
		return (self.__w, self.__h)

	@size.setter
	def size(self, size):
		(self.__w, self.__h) = (size[0], size[1])

	#center
	@property
	def center(self):
		return (self.__x + self.__w/2, self.__y + self.__h/2)

	@center.setter
	def center(self, h):
		(self.__x, self.__y) = (h[0] - self.__w/2, h[1] - self.__h/2)

	#topleft
	@property
	def topleft(self):
		return (self.__x, self.__y)

	@topleft.setter
	def topleft(self, h):
		(self.__x, self.__y) = (h[0], h[1])

	#topright
	@property
	def topright(self):
		return (self.__x  + self.__w, self.__y)

	@topright.setter
	def topright(self, h):
		(self.__x, self.__y) = (h[0] - self.__w, h[1])

	#bottomleft
	@property
	def bottomleft(self):
		return (self.__x, self.__y + self.__h)

	@bottomleft.setter
	def bottomleft(self, h):
		(self.__x, self.__y) = (h[0], h[1] - self.__h)

	#bottomright
	@property
	def bottomright(self):
		return (self.__x  + self.__w, self.__y  + self.__h)

	@bottomright.setter
	def bottomright(self, h):
		(self.__x, self.__y) = (h[0] - self.__w, h[1] - self.__h)

	#midleft
	@property
	def midleft(self):
		return (self.__x, self.__y  + self.__h/2)

	@midleft.setter
	def midleft(self, h):
		(self.__x, self.__y) = (h[0], h[1] - self.__h/2)

	#midright
	@property
	def midright(self):
		return (self.__x  + self.__w, self.__y  + self.__h/2)

	@midright.setter
	def midright(self, h):
		(self.__x, self.__y) = (h[0] - self.__w, h[1] - self.__h/2)

	#midtop
	@property
	def midtop(self):
		return (self.__x  + self.__w/2, self.__y)

	@midtop.setter
	def midtop(self, h):
		(self.__x, self.__y) = (h[0] - self.__w/2, h[1])

	#midbottom
	@property
	def midbottom(self):
		return (self.__x  + self.__w/2, self.__y  + self.__h)

	@midbottom.setter
	def midbottom(self, h):
		(self.__x, self.__y) = (h[0] - self.__w/2, h[1] - self.__h)

	#centerx
	@property
	def centerx(self):
		return self.__x  + self.__w/2

	@centerx.setter
	def centerx(self, cx):
		self.__x = cx - self.__w/2

	#centery
	@property
	def centery(self):
		return self.__y  + self.__h/2

	@centery.setter
	def centery(self, cy):
		self.__y = cy - self.__h/2

	#width
	@property
	def width(self):
		return self.__w

	@width.setter
	def width(self, wth):
		self.__w = wth

	#height
	@property
	def height(self):
		return self.__h

	@height.setter
	def height(self, hgt):
		self.__h = hgt