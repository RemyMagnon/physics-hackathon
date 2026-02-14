from Atom import *
import radioactivedecay as rd


for i in atoms:
    particle = Atom(i, x=None, y=None, radius=5)
    print("-------------")
    print(particle.name)
    print(particle.type)
    print(particle.half_life_readable)
    print(particle.decay_type)
    print(particle.decays_into)