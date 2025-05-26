import pyglet
from utils.animations_loader import load_all_animations

class Player:
    def __init__(self, hero_class, window):
        # Basic attributes
        self.name = hero_class["name"]
        self.flavor = hero_class["flavor"]
        self.stats = hero_class["stats"]
        self.equipment = hero_class["equipment"]
        self.abilities = hero_class["abilities"]

        # Position and movement
        self.x = window.width // 2
        self.y = window.height // 2
        self.dx = 0
        self.dy = 0
        self.speed = 200.0

        # Sprite orientation: 1 for right, -1 for left
        self.scale_x = 1

        # Load animations
        self.animations = load_all_animations(self.name)
        self.current_animation = f'{self.name.lower()} idle'  # e.g., 'necromancer idle'
        self.sprite = self.animations[self.current_animation]
        self.sprite.x = window.width  // 2
        self.sprite.y = window.height // 2
        self.sprite.scale_x = self.scale_x

        self.sprite.draw()

    def update(self, dt, keys_held):
        # Reset movement
        self.dx = 0
        self.dy = 0

        # Vertical movement
        if keys_held.get(pyglet.window.key.W):
            self.dy = self.speed
        if keys_held.get(pyglet.window.key.S):
            self.dy = -self.speed

        # Horizontal movement and orientation
        if keys_held.get(pyglet.window.key.A):
            self.dx = -self.speed
            self.scale_x = -1  # Face left
        elif keys_held.get(pyglet.window.key.D):
            self.dx = self.speed
            self.scale_x = 1   # Face right

        # Apply orientation to sprite
        self.sprite.scale_x = abs(self.sprite.scale_x) * self.scale_x

        # Determine correct animation
        action = 'walk' if (self.dx != 0 or self.dy != 0) else 'idle'
        new_anim_key = f'{self.name.lower()} {action}'

        # Switch animation if needed
        if new_anim_key != self.current_animation:
            self.current_animation = new_anim_key
            self.sprite = self.animations[self.current_animation]
            self.sprite.x = self.x
            self.sprite.y = self.y
            self.sprite.scale_x = self.scale_x

        # Update position
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.sprite.x = self.x
        self.sprite.y = self.y

    # def attack(direction, ):

    def draw(self):
        self.sprite.draw()
        


    def use_ability(self, index):
        if 0 <= index < len(self.abilities):
            print(f"{self.name} used ability: {self.abilities[index]}")
        else:
            print("Invalid ability index")

    def print_stats(self):
        print(f"Class: {self.name}")
        print("Stats:")
        for k, v in self.stats.items():
            print(f"  {k.capitalize()}: {v}")
        print("Abilities:", ", ".join(self.abilities))
