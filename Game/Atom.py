# Updated Nucleon subclass
import random
import pygame
import math
from Constants import *
from Particle import Particle
import radioactivedecay as rd
from enum import Enum, auto
import numpy as np

atoms = ["u",
        "d",
        "n",
        "H-1",
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
        self.name = name
        if name not in atoms:
            raise TypeError("Not a valid atom! Check Atom.py for a full list.")
        elif name == "u":
            self.type = "quark"
            self.identity = "up quark"
            self.id = 10**6/3 + 2*10**3/3
            self.proton_number = 0
            self.neutron_number = 0
            self.half_life = float("inf")
            self.half_life_readable = float("inf")
            self.decays_into = []
            self.decay_type = []
            self.info = "Placeholder text."
        elif name == "d":
            self.type = "quark"
            self.identity = "down quark"
            self.id = 10**6/3 - 10**3/3
            self.proton_number = 0
            self.neutron_number = 0
            self.half_life = float("inf")
            self.half_life_readable = float("inf")
            self.decays_into = []
            self.decay_type = []
            self.info = "Placeholder text."
        elif name == "n":
            self.type = "neutron"
            self.identity = "neutron"
            self.id = 10000000
            self.proton_number = 0
            self.neutron_number = 0
            self.half_life = float("inf")
            self.half_life_readable = float("inf")
            self.decays_into = []
            self.decay_type = []
            self.info = "Placeholder text."
        else:
            self.type = "atom"
            self.identity = rd.Nuclide(name)
            self.id = self.identity.id
            self.proton_number = self.identity.Z
            self.neutron_number = self.identity.A - self.identity.Z
            self.half_life = self.identity.half_life()
            self.half_life_readable = self.identity.half_life("readable")
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

    def merge(self, other):
        if not isinstance(other, Atom):
            return None
        elif other.type and self.type == "atom" or "neutron":
            sum = str(rd.Nuclide(self.id + other.id))
            str_start = sum.index("Nuclide: ")
            str_end = sum.index(", decay")
            sum = sum[str_start + 9:str_end]
            return Atom(sum)
        else: 
            return None
    
    def quarkmerge(self, other1, other2):
        if not isinstance(other1, Atom) or not isinstance(other2, Atom):
            return None
        elif self.type and other1.type and other2.type == "quark":
            ID = self.id + other1.id + other2.id
            if ID == 10010000 or 10000000:
                sum = str(rd.Nuclide(ID))
                str_start = sum.index("Nuclide: ")
                str_end = sum.index(", decay")
                sum = sum[str_start + 9:str_end]
                return Atom(sum)
            else: 
                return None
        else: 
            return None

   
    def __str__(self):
        return self.name  

