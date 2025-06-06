import pyglet
from entities.player.player import PlayerBase
from entities.player.classes.archer.arrow import Arrow
from entities.player.classes.archer.rain_of_arrows import rain_of_arrows
import random

class Archer(PlayerBase):
    def __init__(self, hero_class, window):
        super().__init__(hero_class, window)
        self.window = window
        self.max_arrows = 30

        # Arm
        self.arm_image = pyglet.image.load('assets/arm.png')
        self.arm_image.anchor_x = 0
        self.arm_image.anchor_y = 0
        self.sprite_arm = pyglet.sprite.Sprite(self.arm_image)

        # Body
        self.sprite = pyglet.shapes.Rectangle(self.x, self.y, 20, 60, color=(0, 0, 255))

        # Pull strength bars
        self.pull_low = pyglet.shapes.Rectangle(self.x + 5, self.y - 30, 40, 6, color=(255, 0, 0))
        self.pull_high = pyglet.shapes.Rectangle(self.x + 5, self.y - 30, 0, 6, color=(0, 255, 0))

        # Combat
        self.pull_strength = 0.0
        self.max_pull = 1000
        self.is_pulling = False
        self.arrows = []
        self.ability_arrows = []
        self.using_ability = False

        self.arrows_label = pyglet.text.Label(
            '',
            x=self.x - 10, y=self.y - 35,
            font_name='Consolas',
            font_size=14,
            anchor_x='left', anchor_y='bottom',
            color=(255, 255, 255, 255)
        )

    def update(self, dt, keys_held, map_pixel_width, map_pixel_height, angle):
        super().update(dt, keys_held, map_pixel_width, map_pixel_height, angle)


        # Arm rotation
        self.sprite_arm.rotation = -90 if self.using_ability else angle

        if self.is_pulling:
            self.pull_strength = min(self.pull_strength + 2000 * dt, self.max_pull * 3)
            self.pull_high.width = int(40 * ((self.pull_strength / self.max_pull) / 3))
            self.use_stamina(0.05)
        else:
            self.pull_high.width = 0
            self.pull_strength = 0

        # Update arrows
        player_box = pyglet.shapes.Rectangle(
            self.x, self.y,
            self.sprite.width, self.sprite.height,
            color=(0, 0, 255)
        )

        self.arrows_label.text = f"{self.max_arrows - len(self.arrows)}"
        for arrow in self.arrows[:]:
            if self.check_collision(player_box, arrow.sprite) and arrow.landed:
                self.arrows.remove(arrow)
            else:
                arrow.update(dt)

        for arrow in self.ability_arrows[:]:
            arrow.update(dt)

    def check_collision(self, rect1, rect2):
        return (
            rect1.x < rect2.x + rect2.width and
            rect1.x + rect1.width > rect2.x and
            rect1.y < rect2.y + rect2.height and
            rect1.height + rect1.y > rect2.y
        )

    def draw(self):

        for arrow in self.arrows:
            arrow.draw()

        for arrow in self.ability_arrows:
            arrow.draw()

        # Body
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw()

        # Arm jitter on max pull
        offset_x = random.uniform(-1.5, 1.5) if self.pull_strength >= self.max_pull * 3 else 0
        offset_y = random.uniform(-1.5, 1.5) if self.pull_strength >= self.max_pull * 3 else 0

        self.sprite_arm.x = self.x + self.sprite.width // 2 + offset_x
        self.sprite_arm.y = self.y + self.sprite.height // 2 + offset_y
        self.sprite_arm.draw()

        # Pull bars
        self.pull_low.x = self.x + 5
        self.pull_low.y = self.y - 30
        self.pull_high.x = self.x + 5
        self.pull_high.y = self.y - 30
        self.pull_low.draw()
        self.pull_high.draw()

        # Label
        self.arrows_label.x = self.x - 10
        self.arrows_label.y = self.y - 35
        self.arrows_label.draw()

    def use_ability(self, ability_index, tar_x, tar_y):
        if ability_index < len(self.abilities):
            if ability_index == 0:
                self.using_ability = True
                self.sprite_arm.rotation = 0

                rain_of_arrows(
                    self.x, self.y,
                    tar_x, tar_y,
                    ability_index,
                    window=self.window,
                    arrows_list=self.ability_arrows
                )

                total_duration = (10 - 1) * 0.08 + 1.5 + 0.5 + 0.2
                pyglet.clock.schedule_once(lambda dt: setattr(self, 'using_ability', False), total_duration)

    def start_pull(self):
        if len(self.arrows) < self.max_arrows:
            self.is_pulling = True

    def release_arrow(self, _, target_x, target_y):
        self.is_pulling = False
        if self.pull_strength <= 0 or len(self.arrows) >= self.max_arrows:
            return

        strength_factor = self.pull_strength / self.max_pull
        # Transform mouse coords to world space
        cam_x = self.x - self.window.width // 2
        cam_y = self.y - self.window.height // 2
        real_mouse_x = target_x + cam_x
        real_mouse_y = target_y + cam_y
        
        # Use the logical player position as the arrow's starting point
        arrow = Arrow(
            self.x,  # Use logical position, not sprite position
            self.y,
            real_mouse_x,
            real_mouse_y,
            strength_factor
        )

        self.arrows.append(arrow)
        self.pull_strength = 0


