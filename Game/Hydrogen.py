# Updated Quark subclass
import random
import math
import pygame
from Constants import *
from Particle import Particle
from Atom import Atom

class Hydrogen(Atom):
    def __init__(self,x,y,num_protons=1, num_neutrons=0):
        super().__init__(x,y, num_protons, num_neutrons, radius=HYDROGEN_RADIUS)

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def draw(self, surface):
        import Game
        color = (255, 255, 255)
        pygame.draw.circle(surface, color,
                           (int(self.x), int(self.y)), self.radius)
        label = "²H"
        text = Game.font.render(label, True, (100, 100, 100))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)
