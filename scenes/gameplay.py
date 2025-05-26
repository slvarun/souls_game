from entities.player.player import Player
from entities.player.player_classes import HERO_CLASSES
from pyglet.window import key, mouse


class GamePlayScene:
    def __init__(self, window, class_index):
        self.window = window
        self.keys_held = {}
        self.player = Player(HERO_CLASSES[class_index])

    def draw(self):
        self.player.draw()

    def update(self, dt):
        self.player.update(dt, self.keys_held)

    def on_key_press(self, symbol, modifiers):
        self.keys_held[symbol] = True
        if symbol == key.SPACE:
            self.player.use_ability(0)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.keys_held:
            self.keys_held[symbol] = False

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass
