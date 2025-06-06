import pyglet
import math
from uuid import uuid4

class Arrow:
    GRAVITY = 600

    def __init__(self, x, y, target_x, target_y, strength_factor):

        self.image = pyglet.image.load('assets/arm.png')
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y)
        dx = (target_x) - x
        dy = (target_y) - y
        dx *= strength_factor 
        dy *= strength_factor 

        self.target_x = x + dx
        self.target_y = y + dy

        self.flight_time = 0.8  # seconds
        self.vx = dx / self.flight_time
        self.vy = (dy + 0.5 * self.GRAVITY * self.flight_time ** 2) / self.flight_time

        self.elapsed_time = 0
        self.landed = False

        self.sprite.rotation = -math.degrees(math.atan2(self.vy, self.vx))

    def update(self, dt):
        if self.landed:
            return

        self.elapsed_time += dt
        if self.elapsed_time >= self.flight_time:
            self.sprite.x = self.target_x
            self.sprite.y = self.target_y
            self.vx = 0
            self.vy = 0
            self.landed = True
            return

        self.vy -= self.GRAVITY * dt
        self.sprite.x += self.vx * dt
        self.sprite.y += self.vy * dt
        self.sprite.rotation = -math.degrees(math.atan2(self.vy, self.vx))


    def draw(self):

        self.sprite.draw()
