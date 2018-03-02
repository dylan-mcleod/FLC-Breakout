#!/usr/bin/env python3

import engine
import scenes
import pygame
import os

#load some stuff
engine.load_font("Main Font", "Orbitron-Bold")
engine.load_image("ball", "ball")
engine.load_image("paddle", "paddle")

#for testing, can be removed
engine.get_image("paddle")
engine.get_font("Main Font", 22)

if __name__ == "__main__":
	engine.run(scenes.MainMenuScene())
