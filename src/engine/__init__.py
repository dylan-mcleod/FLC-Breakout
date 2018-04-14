import engine.core
import engine.entity
import engine.ui
import engine.graphics
import engine.io
import engine.collision

#general class definitions
engine.Scene = engine.core.Scene
engine.Entity = engine.entity.Entity
engine.Anchor = engine.graphics.Anchor
engine.SRect = engine.graphics.SRect

#UI class definitions
engine.UIFrame = engine.ui.UIFrame
engine.UIGroup = engine.ui.UIGroup
engine.UIText = engine.ui.UIText
engine.UITextButton = engine.ui.UITextButton
engine.UIMenu = engine.ui.UIMenu
#UI constant definitions
engine.GAME_FONT = engine.ui.GAME_FONT
engine.GAME_FONT_BOLD = engine.ui.GAME_FONT_BOLD
engine.GAME_FONT_COLOR = engine.ui.GAME_FONT_COLOR
engine.GAME_FONT_COLOR_ACTIVE = engine.ui.GAME_FONT_COLOR_ACTIVE
engine.GAME_FONT_COLOR_DISABLED = engine.ui.GAME_FONT_COLOR_DISABLED
engine.GAME_MENU_BG_COLOR = engine.ui.GAME_MENU_BG_COLOR
engine.DEFAULT_MENU_PADDING = engine.ui.DEFAULT_MENU_PADDING
engine.DEFAULT_FONT_HEIGHT = engine.ui.DEFAULT_FONT_HEIGHT

#graphics
engine.get_screen_bounds = engine.graphics.get_screen_bounds
#DEPRECATED (but necessary for UI)
engine.to_engine_units = engine.graphics.to_engine_units
#DEPRECATED
engine.to_pygame_units = engine.graphics.to_pygame_units
#engine.get_window_scale = engine.graphics.get_window_scale
#engine.get_window_bounds = engine.graphics.get_window_bounds

#Scene management methods
engine.run = engine.core.sceneManager.run
engine.add_scene = engine.core.sceneManager.add_scene
engine.switch_scene = engine.core.sceneManager.switch_scene
engine.replace_scene = engine.core.sceneManager.replace_scene
engine.exit_scene = engine.core.sceneManager.exit_scene

#common keyboard input queries
engine.was_key_pressed = engine.core.keyboardManager.was_key_pressed
engine.isKeyDown = engine.core.keyboardManager.is_key_down

#common mouse input queries
engine.get_clicks = engine.core.mouseManager.get_clicks
engine.get_mouse_position = engine.core.mouseManager.get_mouse_position

#virtual mode mouse queries
engine.get_mouse_movement = engine.core.mouseManager.get_mouse_movement
engine.get_virtual_mode = engine.core.mouseManager.get_virtual_mode
engine.enter_virtual_mode = engine.core.mouseManager.enter_virtual_mode
engine.leave_virtual_mode = engine.core.mouseManager.leave_virtual_mode
#Disabled due to bad practice/readability. Uncomment if you need to use one of these methods.
#engine.set_virtual_mode = engine.core.mouseManager.set_virtual_mode
#engine.set_mouse_position = engine.core.mouseManager.set_mouse_position

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

engine.check_collide = engine.collision.check_collide

engine.ui.initialize_ui()
