import pygame
import engine
import scenes

class PauseScene(engine.Scene):

	def __init__(self):
		pass


	def update(self, delta):
		#temporary, left click to resume
		if(engine.getClicks()[0]): engine.exitScene()
		#temporary, right click to go to main menu
		if(engine.getClicks()[2]): engine.replaceScene(scenes.MainMenuScene())
		#press escape to unpause
		if engine.wasKeyPressed(pygame.K_ESCAPE): engine.exitScene()



	def render(self, surface):
		#white, semi-transparent background
		surface.fill((255,255,255,120))


	def pause(self):
		pass