# Updated Nucleon subclass
import random
import pygame
import math
from Constants import *
from Particle import Particle

class Atom(Particle):
    def __init__(self, x, y, num_protons, num_neutrons, radius):
        super().__init__(x, y, radius)
        self.num_protons = num_protons
        self.num_neutrons = num_neutrons
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        self.apply_gravity(strength_multiplier=0.85)
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor
        self.update_position()

    def draw(self, surface):
        pass
