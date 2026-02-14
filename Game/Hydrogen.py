# Updated Quark subclass
import random
import math
import pygame
from Constants import *
from Particle import Particle
from Atom import Atom

class Hydrogen(Atom):
    def __init__(self,x,y,num_protons=1, num_neutrons=0):

        if(num_protons != 1 and num_neutrons == 1):
            self.type = "H-2"
        else:
            self.type = "H-1"
        super().__init__(self.type, x,y, radius=HYDROGEN_RADIUS)

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def draw(self, surface):
        import Game
        color = (255, 255, 255)
        pygame.draw.circle(surface, color,
                           (int(self.x), int(self.y)), self.radius)
        if(self.type == "H-1"):
             label = "¹H"
        elif(self.type == "H-2"):
            label = "²H"
        else:
            label = "H"
        text = Game.font.render(label, True, (100, 100, 100))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)
