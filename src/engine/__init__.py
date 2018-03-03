import engine.core
import engine.entity
import engine.ui
import engine.scaling
import engine.io

#class definitions
engine.Scene = engine.core.Scene
engine.Entity = engine.entity.Entity
engine.Anchor = engine.scaling.Anchor
engine.SRect = engine.scaling.SRect

#User interfaces
engine.GAME_FONT = engine.ui.GAME_FONT
engine.GAME_FONT_BOLD = engine.ui.GAME_FONT_BOLD
engine.UI_Frame = engine.ui.UI_Frame
engine.UI_Group = engine.ui.UI_Group
engine.UI_Text = engine.ui.UI_Text
engine.UI_Text_Button = engine.ui.UI_Text_Button
engine.UI_Menu = engine.ui.UI_Menu

#scaling
engine.screen_bounds = engine.scaling.screen_bounds
engine.window_scale = engine.scaling.window_scale
engine.window_bounds = engine.scaling.window_bounds
engine.to_engine_units = engine.scaling.to_engine_units
engine.to_pygame_units = engine.scaling.to_pygame_units

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



#asset management
engine.load_image = engine.io.assetManager.load_image
engine.get_image = engine.io.assetManager.get_image

engine.load_font = engine.io.assetManager.load_font
engine.get_font = engine.io.assetManager.get_font

engine.load_sfx = engine.io.assetManager.load_sfx
engine.get_sfx = engine.io.assetManager.get_sfx

engine.load_music = engine.io.assetManager.load_music
engine.get_music = engine.io.assetManager.get_music

#Disabled due to bad practice/readability. Uncomment if you need to use one of these methods.
#engine.AssetType = engine.io.AssetType
#engine.add_asset = engine.io.assetManager.add_asset
#engine.get_asset_path = engine.io.assetManager.get_asset_path

engine.ui.initialize_ui()
