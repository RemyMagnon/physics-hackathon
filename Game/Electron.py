import random
import math
import pygame
from Constants import *
from Particle import Particle

class Electron(Particle):
    def __init__(self):
        super().__init__(radius=ELECTRON_RADIUS)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(self):
        self.apply_gravity()
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor
        self.update_position()

    def draw(self, surface):
        import Game
        pygame.draw.circle(surface, (255, 255, 100), (int(self.x), int(self.y)), self.radius)
        text = Game.font.render("e", True, (0, 0, 0))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)