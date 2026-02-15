# Updated Quark subclass
import random
import math
import pygame
from Constants import *
from Particle import Particle

class Quark(Particle):
    def __init__(self, flavor):
        super().__init__()
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.flavor = flavor

    def update(self):
        self.apply_gravity()
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor
        self.update_position()

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def draw(self, surface):
        import Game
        color = (255, 100, 100) if self.flavor == "up" else (100, 150, 255)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        label = "u" if self.flavor == "up" else "d"
        text = Game.font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)
