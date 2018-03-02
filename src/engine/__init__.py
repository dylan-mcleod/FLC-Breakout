import engine.core
import engine.entity
import engine.ui
import engine.scaling
import engine.io

#class definitions
engine.Scene = engine.core.Scene
engine.Entity = engine.entity.Entity
engine.Text = engine.ui.Text
engine.Menu = engine.ui.Menu

#Common Utilities
engine.Anchor = engine.scaling.Anchor
engine.SRect = engine.scaling.SRect
engine.screen_bounds = engine.scaling.screen_bounds

engine.window_bounds = engine.scaling.window_bounds

#Scene management methods
engine.run = engine.core.sceneManager.run
engine.addScene = engine.core.sceneManager.addScene
engine.switchScene = engine.core.sceneManager.switchScene
engine.replaceScene = engine.core.sceneManager.replaceScene
engine.exitScene = engine.core.sceneManager.exitScene

#common keyboard input queries
engine.wasKeyPressed = engine.core.keyboardManager.wasKeyPressed
engine.isKeyDown = engine.core.keyboardManager.isKeyDown

#common mouse input queries
engine.getClicks = engine.core.mouseManager.getClicks
engine.getMousePosition = engine.core.mouseManager.getMousePosition

#virtual mode mouse queries
engine.getMouseMovement = engine.core.mouseManager.getMouseMovement
engine.getVirtualMode = engine.core.mouseManager.getVirtualMode
engine.enterVirtualMode = engine.core.mouseManager.enterVirtualMode
engine.leaveVirtualMode = engine.core.mouseManager.leaveVirtualMode

#Disabled due to bad practice/readability. Uncomment if you need to use one of these methods.
#engine.setVirtualMode = engine.core.mouseManager.setVirtualMode
#engine.setMousePosition = engine.core.mouseManager.setMousePosition

engine.AssetType = engine.io.AssetType
engine.add_asset = engine.io.assetManager.add_asset
engine.get_asset_path = engine.io.assetManager.get_asset_path
