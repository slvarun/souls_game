from pyglet.window import key
from scenes.gameplay import GamePlayScene
import pyglet



class MainMenuScene:
    def __init__(self, window):
        self.window = window
        self.label = pyglet.text.Label('Main Menu - Press ENTER',
                                       font_size=36,
                                       x=window.width//2,
                                       y=window.height//2,
                                       anchor_x='center',
                                       anchor_y='center')

    def draw(self):
        self.label.draw()

    def update(self, dt):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.window.current_scene = GamePlayScene(self.window, class_index="necromancer")

    def on_key_release(self, symbol, modifiers): pass
    def on_mouse_press(self, x, y, button, modifiers): pass
    def on_mouse_motion(self, x, y, dx, dy): pass
