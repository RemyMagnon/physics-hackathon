# Updated Nucleon subclass
import random
import pygame
import math
from Constants import *
from Particle import Particle
import radioactivedecay as rd
from enum import Enum, auto
import numpy as np

atoms = ["H-1",
        "H-2",
        "H-3",
        "He-3",
        "He-4",
        "Li-6",
        "Li-7",
        "Be-7",
        "B-10",
        "Be-10",
        "B-11",
        "C-10",
        "C-11",
        "N-13",
        "O-14",
        "C-12",
        "C-13",
        "C-14",
        "N-14",
        "O-16",
        "O-15",
        "O-17",
        "O-18",
        "F-19",
        "F-18",
        "Ne-20"]


class Atom(Particle):
    def __init__(self, name, x, y, radius):
        super().__init__(x, y, radius)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        if name not in atoms:
            raise TypeError("Not a valid atom! Check Atom.py for a full list.")
        self.identity = rd.Nuclide(name)
        self.id = self.identity.id
        self.proton_number = self.identity.Z
        self.neutron_number = self.identity.A - self.identity.Z

        self.decays_into = self.identity.progeny()
        self.decay_type = self.identity.decay_modes()
        self.info = "Placeholder text."

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


    @staticmethod
    def merge(a1, a2):
        if not isinstance(a2, Atom):
            return None
        sum = str(rd.Nuclide(a1.id + a2.id))
        str_start = sum.index("Nuclide: ")
        str_end = sum.index(", decay")
        sum = sum[str_start + 9:str_end]
        return Atom(sum)
   
    def __str__(self):
        return self.name

