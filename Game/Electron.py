import random
import math
import pygame
from Constants import *

class Electron:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(0.5, 1)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = 5
        self.destroy = False

    def update(self):
        import Game
        if Game.gravity_active:
            dx = Game.gravity_pos[0] - self.x
            dy = Game.gravity_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                force = GRAVITY_STRENGTH / (dist * dist)
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force

        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, surface):
        import Game
        pygame.draw.circle(surface, (255, 255, 100), (int(self.x), int(self.y)), self.radius)
        text = Game.font.render("e", True, (0, 0, 0))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)