from entities.player.player import Player
from entities.player.player_classes import HERO_CLASSES
from pyglet.window import key, mouse
import pyglet

class GamePlayScene:
    def __init__(self, window, class_index):
        self.window = window
        self.keys_held = {}

        # Initialize player in the middle of the map (world coords):
        start_x = 2000 // 2
        start_y = 2000 // 2
        self.player = Player(HERO_CLASSES[class_index], window)

        # Camera offsets
        self.camera_x = 0
        self.camera_y = 0

        # HUD label
        self.coord_label = pyglet.text.Label(
            '',
            font_name='Consolas',
            font_size=14,
            x=10, y=50,
            anchor_x='left', anchor_y='bottom',
            color=(255,255,255,255)
        )

        # Map size in pixels
        self.map_pixel_width  = 2000
        self.map_pixel_height = 2000

    def update(self, dt):
        # 1) Update player world position
        self.player.update(dt, self.keys_held)
        self.player.x = max(0, min(self.player.x, self.map_pixel_width))
        self.player.y = max(0, min(self.player.y, self.map_pixel_height))


        # 2) Update HUD text
        px, py = self.player.x, self.player.y
        self.coord_label.text = f"Map X: {px:.1f}  Y: {py:.1f}"

        # 3) Recompute camera so player is centered
        self.camera_x = (self.window.width  // 2) - px
        self.camera_y = (self.window.height // 2) - py

        # 4) Clamp to map bounds
        self.camera_x = min(0, max(self.camera_x, self.window.width  - self.map_pixel_width))
        self.camera_y = min(0, max(self.camera_y, self.window.height - self.map_pixel_height))

    def draw(self):
        # 1) Draw map (placeholder loop)
        # for tile in self.map.tiles:
        #     screen_x = tile.world_x + self.camera_x
        #     screen_y = tile.world_y + self.camera_y
        #     tile.sprite.x, tile.sprite.y = screen_x, screen_y
        #     tile.sprite.draw()

        # 2) Draw other entities similarly...
        
        # 3) Draw player fixed at screen center
        self.player.sprite.x = self.window.width  // 2
        self.player.sprite.y = self.window.height // 2
        self.player.sprite.draw()

        # 4) Draw HUD last
        self.coord_label.draw()

    def on_key_press(self, symbol, modifiers):
        self.keys_held[symbol] = True
        if symbol == key.SPACE:
            # Use the first ability as an “attack”
            self.player.use_ability(0)

    def on_key_release(self, symbol, modifiers):
        self.keys_held[symbol] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            # Left‐click also triggers ability 0:
            self.player.use_ability(0)

    def on_mouse_motion(self, x, y, dx, dy):
        pass
