#[WIP] - COMPLETELY UNFINISHED
#although some functionality does work correctly.
import pygame
from enum import Enum
import os

class AssetType(Enum):
	IMAGE = 1
	FONT = 2
	SFX = 3
	MUSIC = 4

class AssetManager:

	def __init__(self):
		self.asset_list = {}
		for t in AssetType:
			self.asset_list[t] = {}
		


	def add_asset(self, name, relpath, atype = None):
		file_name, file_ext = os.path.splitext(getAssetPath(relpath))

		try:
			if(not atype):
				if  (file_ext == ".png"): atype = AssetType.IMAGE
				elif(file_ext == ".ttf"): atype = AssetType.FONT
				elif(file_ext == ".wav"): atype = AssetType.SFX
				elif(file_ext == ".ogg"): atype = AssetType.MUSIC
			self.asset_list[atype][name] = getAssetPath(relpath)
		except IOError as error:
			print("WARNING!: File \"{}\" not found!".format(relpath))
			return False
		return True

	def get_asset_path(self, name, atype = None):
		if(not atype):
			#TODO: try everything?
			pass
		return self.asset_list[atype][name]

	def get_image(self, name):
		pass

	def get_font(self, name, size):
		return pygame.font.Font(self.asset_list[AssetType.FONT][name], size)

	def get_sfx(self, name):
		pass

	def get_music(self, name):
		pass




def getAssetPath(relpath):
	return os.path.abspath(os.path.join("..", "assets",relpath))

def getDataPath(relpath):
	return os.path.abspath(os.path.join("..", "data", relpath))

assetManager = AssetManager()
