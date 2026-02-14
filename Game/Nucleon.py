# Updated Nucleon subclass
import random
import pygame
import math
from Constants import *
from Particle import Particle

class Nucleon(Particle):
    def __init__(self, x, y, kind):
        super().__init__(x, y, radius=NUCLEON_RADIUS)
        self.kind = kind
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        self.apply_gravity(strength_multiplier=NUCLEON_ATTRACTION_MULTIPLIER)
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor
        self.update_position()

    def draw(self, surface):
        import Game
        label=""
        if(self.kind == "proton"):
            color = (255, 80, 80) 
            label = "P" 
        else:            
            color = (80, 80, 255)
            label = "N"
        pygame.draw.circle(surface, color,
                           (int(self.x), int(self.y)), self.radius)
        text = Game.font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)
