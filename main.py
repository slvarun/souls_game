import pyglet
from pyglet.window import key, mouse
from scenes.menu import MainMenuScene

class GameWindow(pyglet.window.Window):
    def __init__(self, width=1280, height=720, title="My Pyglet Game"):
        super().__init__(width, height, title)
        self.set_location(100, 100)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.current_scene = MainMenuScene(self)

    def on_draw(self):
        self.clear()
        self.current_scene.draw()
        self.fps_display.draw()

    def update(self, dt):
        self.current_scene.update(dt)

    def on_key_press(self, symbol, modifiers):
        self.current_scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.current_scene.on_key_release(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.current_scene.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.current_scene.on_mouse_motion(x, y, dx, dy)

if __name__ == "__main__":
    window = GameWindow()
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()
