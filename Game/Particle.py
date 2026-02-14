# Particle superclass
import random
import math
from Constants import *

class Particle:
    def __init__(self, x=None, y=None, radius=5):
        if x is not None:
            self.x = x
        else:
            self.x = random.uniform(0, WIDTH)

        if y is not None:
            self.y = y
        else:
            self.y = random.uniform(0, HEIGHT)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.radius = radius
        self.destroy = False

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT

    def apply_gravity(self, strength_multiplier=1.0):
        import Game
        if Game.gravity_active:
            dx = Game.gravity_pos[0] - self.x
            dy = Game.gravity_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                force = (GRAVITY_STRENGTH * strength_multiplier) / (dist ** 2)
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force
