import engine
import scenes
import pygame
import os

print(os.path.abspath(os.path.join("src\\", os.pardir)))
print(os.pardir)
print(os.path.abspath(os.path.join("..\\assets\\","fonts")))

engine.add_asset("Main Font", "fonts\\Orbitron-Bold.ttf")
print(engine.get_asset_path("Main Font", engine.AssetType.FONT))

if __name__ == "__main__":
	engine.run(scenes.MainMenuScene())