import pyglet

class MainMenuScene:
    def __init__(self, window):
        self.window = window
        self.label = pyglet.text.Label('Main Menu',
                                       font_size=36,
                                       x=window.width//2,
                                       y=window.height//2,
                                       anchor_x='center',
                                       anchor_y='center')

    def draw(self):
        self.label.draw()

    def update(self, dt):
        pass  # Could animate or do menu logic

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            print("Start Game")

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass
