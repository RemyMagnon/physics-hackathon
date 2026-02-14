# Updated Nucleon subclass
import random
import math
from Constants import *
from Atom import Atom

class Nucleon(Atom):
    def __init__(self,name, x, y):
        super().__init__(name,x, y, radius=NUCLEON_RADIUS)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.merge_timer = 0  # Timer to track how long nucleons stick together
        self.merge_group_id = None  # ID of the group this nucleon is trying to merge with

    def update(self):
        self.apply_gravity(strength_multiplier=NUCLEON_ATTRACTION_MULTIPLIER)
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor
        self.update_position()
