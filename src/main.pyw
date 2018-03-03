#!/usr/bin/env python3

import engine
import scenes
import pygame
import os

#load the (temporary?) background image ;)
engine.load_image("metal background", os.path.join("backgrounds", "metal_background.jpg"))

#for testing, can be removed

if __name__ == "__main__":
	engine.run(scenes.MainMenuScene())
