from entities.player.classes.archer.archer import Archer
from entities.player.player_classes import HERO_CLASSES
from pyglet.window import key, mouse
import pyglet
from math import degrees, atan2
from pyglet.math import Mat4, Vec3


class GamePlayScene:
    def __init__(self, window, class_index):
        self.window = window
        self.player = Archer(HERO_CLASSES[class_index], window)

        # Zoom & camera
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        self.zoom_lerp_speed = 2.0
        self.max_zoom_out = 0.4
        self.camera_x = 0
        self.camera_y = 0

        # Input
        self.keys_held = {}

        # Angle calculation
        self.current_angle = 0

        # World dimensions
        self.map_pixel_width = 10000
        self.map_pixel_height = 10000

        # UI labels
        self.coord_label = pyglet.text.Label(
            '',
            font_name='Consolas',
            font_size=14,
            x=10, y=50,
            anchor_x='left', anchor_y='bottom',
            color=(255, 255, 255, 255)
        )
        self.angle_label = pyglet.text.Label(
            '',
            font_name='Consolas',
            font_size=14,
            x=10, y=70,
            anchor_x='left', anchor_y='bottom',
            color=(255, 255, 255, 255)
        )

    def update(self, dt):
        # Smooth zoom interpolation
        if abs(self.zoom_level - self.target_zoom) > 0.01:
            direction = 1 if self.zoom_level < self.target_zoom else -1
            self.zoom_level += direction * self.zoom_lerp_speed * dt
            if (direction == 1 and self.zoom_level > self.target_zoom) or \
            (direction == -1 and self.zoom_level < self.target_zoom):
                self.zoom_level = self.target_zoom

        # Angle calculation based on mouse position
        mouse_x, mouse_y = self.window._mouse_x, self.window._mouse_y
        dx = mouse_x - (self.window.width // 2)
        dy = mouse_y - (self.window.height // 2)
        angle = (degrees(atan2(dy, dx)) * -1)
        self.current_angle = angle

        # Update player logic
        self.player.update(dt, self.keys_held, self.map_pixel_width, self.map_pixel_height, angle)

        # Camera position should move to player's position
        self.camera_x = -self.player.x + (self.window.width / 2) / self.zoom_level
        self.camera_y = -self.player.y + (self.window.height / 2) / self.zoom_level

        # Clamp camera to map bounds
        min_x = -(self.map_pixel_width - self.window.width / self.zoom_level)
        max_x = 0
        self.camera_x = max(min(self.camera_x, max_x), min_x)

        min_y = -(self.map_pixel_height - self.window.height / self.zoom_level)
        max_y = 0
        self.camera_y = max(min(self.camera_y, max_y), min_y)

        # Update UI labels
        self.coord_label.text = f"Map X: {self.player.x:.1f}  Y: {self.player.y:.1f}"
        self.angle_label.text = f"{angle:.1f}"

    def draw(self):
        # Apply camera transform
        translate = Mat4.from_translation(Vec3(self.camera_x, self.camera_y, 0))
        scale = Mat4.from_scale(Vec3(self.zoom_level, self.zoom_level, 1))
        self.window.view = scale @ translate

        # Draw world
        self.player.draw()

        # Reset to default view for UI
        self.window.view = Mat4()

        # Draw UI
        self.coord_label.draw()
        self.angle_label.draw()
        self.player.health_bar_bg.draw()
        self.player.health_bar_fg.draw()
        self.player.stamina_bar_bg.draw()
        self.player.stamina_bar_fg.draw()

    def reset_zoom(self, dt):
        self.target_zoom = 1.0

    def on_key_press(self, symbol, modifiers):
        self.keys_held[symbol] = True

        if symbol == key.E :
            mouse_x, mouse_y = self.window._mouse_x, self.window._mouse_y
            self.player.use_ability(0, mouse_x, mouse_y)   
        if symbol == key.Q:
            self.target_zoom = self.max_zoom_out
            pyglet.clock.schedule_once(self.reset_zoom, 7)

    def on_key_release(self, symbol, modifiers):
        self.keys_held[symbol] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.player.start_pull()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.player.release_arrow(self.current_angle, x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        pass
