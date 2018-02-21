import pygame
import engine
import scenes
import pygame.font

class MainMenuScene(engine.Scene):

	def __init__(self):
		pass


	def update(self, delta):
		#for now, just go straight to the play scene on any left click or enter
		if engine.getClicks()[0] or engine.wasKeyPressed(pygame.K_RETURN): engine.switchScene(scenes.PlayScene())



	def render(self, surface):
		#render some example text
		text = pygame.font.Font(pygame.font.match_font('bitstreamverasans'), 22).render("Left click anywhere or press enter to play the game.",True,(255,255,255))
		surface.fill((40,40,40))

		surface.blit(text, text.get_rect())


	def pause(self):
		pass