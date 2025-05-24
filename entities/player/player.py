import pyglet

class Player:
    def __init__(self, hero_class, x=100, y=100):
        self.name = hero_class["name"]
        self.flavor = hero_class["flavor"]
        self.stats = hero_class["stats"]
        self.equipment = hero_class["equipment"]
        self.abilities = hero_class["abilities"]

        # Position and movement
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.speed = 200

        # Load placeholder sprite (replace with real animations)
        self.image = pyglet.resource.image('sprites/player_placeholder.png')
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y)

    def update(self, dt, keys_held):
        self.dx = 0
        self.dy = 0

        if keys_held.get(pyglet.window.key.W):
            self.dy = self.speed
        if keys_held.get(pyglet.window.key.S):
            self.dy = -self.speed
        if keys_held.get(pyglet.window.key.A):
            self.dx = -self.speed
        if keys_held.get(pyglet.window.key.D):
            self.dx = self.speed

        self.x += self.dx * dt
        self.y += self.dy * dt
        self.sprite.set_position(self.x, self.y)

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
