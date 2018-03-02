#[WIP] - COMPLETELY UNFINISHED
#although some functionality does work correctly.
#Note: pygame.mixer is for SFX, pygame.mixer.music is for MUSIC
import pygame
from enum import Enum
import os

class AssetType(Enum):
	#UNDEF = 0
	IMAGE = 1
	FONT = 2
	SFX = 3
	MUSIC = 4

	def __int__(self):
		return self.value

	def __str__(self):
		return ("error", "image", "font", "sfx", "music")[self.value]

def getAssetPath(relpath, atype = None):
	subpath = ""
	if  (atype == AssetType.IMAGE): subpath = "images"
	elif(atype == AssetType.FONT) : subpath = "fonts"
	elif(atype == AssetType.SFX)  : subpath = "sfx"
	elif(atype == AssetType.MUSIC): subpath = "music"

	if(subpath): relpath = os.path.join(subpath, relpath)
	return os.path.join("..", "assets", relpath)

def getDataPath(relpath):
	return os.path.abspath(os.path.join("..", "data", relpath))

class AssetManager:

	def __init__(self):
		self.asset_path_list = {}
		self.image_list = {}
		for t in AssetType:
			self.asset_path_list[t] = {}



	def add_asset(self, name, relpath, atype = None, assumepath = False):
		file_name, file_ext = os.path.splitext(getAssetPath(relpath))

		try:
			if(not atype):
				if  (file_ext == ".png"): atype = AssetType.IMAGE
				elif(file_ext == ".ttf"): atype = AssetType.FONT
				elif(file_ext == ".wav"): atype = AssetType.SFX
				elif(file_ext == ".ogg"): atype = AssetType.MUSIC
				else:
					return False
			if(not file_ext):
				if  (atype == AssetType.IMAGE): file_ext = ".png"
				elif(atype == AssetType.FONT) : file_ext = ".ttf"
				elif(atype == AssetType.SFX)  : file_ext = ".wav"
				elif(atype == AssetType.MUSIC): file_ext = ".ogg"
				else:
					return False
				#now append the extension to the file name
				relpath = relpath + file_ext

			#Add the asset path to the directory of assets
			relpath = getAssetPath(relpath, atype if assumepath else None)
			fullpath = os.path.abspath(relpath)
			self.asset_path_list[atype][name] = fullpath
			#This is here for custom code per asset type
			if  (atype == AssetType.IMAGE):
				#stores image as a pygame.Surface
				self.image_list[name] = pygame.image.load(fullpath)
			elif(atype == AssetType.FONT):
				pass
			elif(atype == AssetType.SFX):
				pass
			elif(atype == AssetType.MUSIC):
				pass

			print("Asset Manager: Loaded {} \"{}\" with path \"{}\".".format(str(atype), name, relpath))
		except IOError as error:
			#This should be changed; I don't think it actually catches anything, plus it's bad
			print("WARNING!: File \"{}\" not found!".format(relpath))
			return False
		return True

	def get_asset_path(self, name, atype = None):
		if(not atype):
			#TODO: try everything?
			pass
		return self.asset_path_list[atype][name]

	#get/load image
	def load_image(self, name, relpath):
		return self.add_asset(name, relpath, AssetType.IMAGE, True)

	def get_image(self, name):
		return self.image_list[name]

	#get/load font
	def load_font(self, name, relpath):
		return self.add_asset(name, relpath, AssetType.FONT, True)

	def get_font(self, name, size):
		return pygame.font.Font(self.asset_path_list[AssetType.FONT][name], size)

	#get/load SFX
	def load_sfx(self, name, relpath):
		return self.add_asset(name, relpath, AssetType.SFX, True)

	def get_sfx(self, name):
		pass

	#get/load music
	def load_music(self, name, relpath):
		return self.add_asset(name, relpath, AssetType.MUSIC, True)

	def get_music(self, name):
		pass

assetManager = AssetManager()