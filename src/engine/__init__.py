import engine.core
import engine.entity

engine.Scene = engine.core.Scene
engine.Entity = engine.entity.Entity

engine.run = engine.core.sceneManager.run
engine.addScene = engine.core.sceneManager.addScene
engine.switchScene = engine.core.sceneManager.switchScene
engine.replaceScene = engine.core.sceneManager.replaceScene
engine.exitScene = engine.core.sceneManager.exitScene

engine.wasKeyPressed = engine.core.keyboardManager.wasKeyPressed
engine.isKeyDown = engine.core.keyboardManager.isKeyDown

engine.getClicks = engine.core.mouseManager.getClicks