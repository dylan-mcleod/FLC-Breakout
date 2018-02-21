import pygame
import math
from pygame.locals import *
from engine import *
from scenes.play import PlayScene

class MainMenuScene(Scene):

	def __init__(self):
		self.paused = False

		self.background = pygame.Surface((800,600))
		self.background.fill((0,0,0))


	def update(self, delta):
		#for now, just go straight to the play scene
		sceneManager.switchScene(PlayScene())
		return



	def render(self):
		screen.blit(self.background,self.background.get_rect())


	def pause(self):
		self.paused = True


	def resume(self):
		self.paused = False