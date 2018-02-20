import pygame
import math
from pygame.locals import *
from engine import *
from scenes.play import PlayScene
from scenes.mainMenu import MainMenuScene


sceneManager.addScene("mainMenu", MainMenuScene())
sceneManager.selectScene("mainMenu")
sceneManager.run()