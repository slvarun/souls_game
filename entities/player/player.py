import pyglet

class PlayerBase:
    def __init__(self, hero_class, window):
        self.name = hero_class["name"]
        self.flavor = hero_class["flavor"]
        self.stats = hero_class["stats"]
        self.equipment = hero_class["equipment"]
        self.abilities = hero_class["abilities"]

        self.x = window.width // 2
        self.y = window.height // 2
        self.dx = 0
        self.dy = 0
        self.speed = 200.0
        self.scale_x = 1
        self.health = self.max_health = self.stats["vigor"] 
        self.endurance = self.max_endurance = self.stats["endurance"]
        self.stamina = self.max_stamina = self.stats["stamina"]
        self.poise = self.max_poise = self.stats["poise"]
        self.strength = self.max_strength = self.stats["strength"]
        self.luck = self.max_luck = self.stats["luck"]
        self.health_regen = 0.001
        self.stamina_regen = 2
        self.stamina_drain_rate = 0.3  # per second while moving

        # Health and Stamina Bars
        self.bar_width = 200
        self.bar_height = 15
        self.health_bar_bg = pyglet.shapes.Rectangle(10, window.height - 30, self.bar_width, self.bar_height, color=(50, 0, 0))
        self.health_bar_fg = pyglet.shapes.Rectangle(10, window.height - 30, self.bar_width, self.bar_height, color=(200, 0, 0))

        self.stamina_bar_bg = pyglet.shapes.Rectangle(10, window.height - 50, self.bar_width, self.bar_height, color=(0, 50, 0))
        self.stamina_bar_fg = pyglet.shapes.Rectangle(10, window.height - 50, self.bar_width, self.bar_height, color=(0, 200, 0))



            
    def update(self, dt, keys_held, map_pixel_width, map_pixel_height, angle):
            self.dx = self.dy = 0
            is_moving = False

            if keys_held.get(pyglet.window.key.W):
                self.dy = self.speed
                is_moving = True
            if keys_held.get(pyglet.window.key.S):
                self.dy = -self.speed
                is_moving = True
            if keys_held.get(pyglet.window.key.A):
                self.dx = -self.speed
                self.scale_x = -1
                is_moving = True
            elif keys_held.get(pyglet.window.key.D):
                self.dx = self.speed
                self.scale_x = 1
                is_moving = True

            # Movement
            self.x += self.dx * dt
            self.y += self.dy * dt

            # Clamp to map
            self.x = max(0, min(self.x, map_pixel_width))
            self.y = max(0, min(self.y, map_pixel_height))

            # Regenerate health
            self.health = min(self.max_health, self.health + self.health_regen * dt)

            # Drain or regen stamina
            if is_moving:
                self.stamina = max(0, self.stamina - self.stamina_drain_rate * dt)
            else:
                self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen * dt)

            # Update bar widths
            self.health_bar_fg.width = (self.health / self.max_health) * self.bar_width
            self.stamina_bar_fg.width = (self.stamina / self.max_stamina) * self.bar_width

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        # You can add death logic here if health <= 0

    def use_stamina(self, amount):
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False

    def print_stats(self):
        print(f"Class: {self.name}")
        print(f"Health: {self.health:.1f} / {self.max_health}")
        print(f"Stamina: {self.stamina:.1f} / {self.max_stamina}")
        for k, v in self.stats.items():
            print(f"  {k.capitalize()}: {v}")
        print("Abilities:", ", ".join(self.abilities))
