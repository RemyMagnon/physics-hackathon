# Updated Nucleon subclass
import random
import pygame
from Particle import Particle

class Nucleon(Particle):
    def __init__(self, x, y, kind):
        import Game
        g = Game
        super().__init__(x, y, radius=g.NUCLEON_RADIUS)
        self.kind = kind
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        self.apply_gravity(strength_multiplier=0.6)
        self.update_position()

    def draw(self, surface):
        import Game
        color = (255, 80, 80) if self.kind == "proton" else (80, 140, 255)
        pygame.draw.circle(surface, color,
                           (int(self.x), int(self.y)), self.radius)
        label = "P" if self.kind == "proton" else "N"
        text = Game.font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)
