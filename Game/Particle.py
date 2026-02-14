# Particle superclass
import random
import math
import pygame

class Particle:
    def __init__(self, x=None, y=None, radius=5):
        import Game
        g = Game
        self.x = x if x is not None else random.uniform(0, g.WIDTH)
        self.y = y if y is not None else random.uniform(0, g.HEIGHT)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.radius = radius
        self.destroy = False

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

        import Game
        g = Game
        self.x %= g.WIDTH
        self.y %= g.HEIGHT

    def apply_gravity(self, strength_multiplier=1.0):
        import Game
        if Game.gravity_active:
            dx = Game.gravity_pos[0] - self.x
            dy = Game.gravity_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                force = (Game.GRAVITY_STRENGTH * strength_multiplier) / (dist * dist)
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force
