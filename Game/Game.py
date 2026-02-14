import pygame
import random
import math
from Constants import *
from Quark import Quark
from Nucleon import Nucleon
from Hydrogen import Hydrogen
from Atom import Atom

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Sandbox - Up & Down Quarks")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

particles = []
gravity_active = False
gravity_pos = (0, 0)


# ---------------- COLLISION ----------------

def resolve_collision(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    dist = math.hypot(dx, dy)

    if dist == 0:
        return

    overlap = a.radius + b.radius - dist
    if overlap > 0:
        nx = dx / dist
        ny = dy / dist

        a.x -= nx * overlap / 2
        a.y -= ny * overlap / 2
        b.x += nx * overlap / 2
        b.y += ny * overlap / 2

        dvx = a.vx - b.vx
        dvy = a.vy - b.vy
        impact_speed = dvx * nx + dvy * ny

        if impact_speed > 0:
            return

        impulse = -impact_speed
        a.vx += impulse * nx
        a.vy += impulse * ny
        b.vx -= impulse * nx
        b.vy -= impulse * ny


def handle_collisions():
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            resolve_collision(particles[i], particles[j])


#    Apply subtle attraction to other clusters based on distance.
#    max_force: max acceleration applied per frame
#    min_distance: distance below which force is capped

def apply_cluster_attraction(nucleon, particles, max_force=-0.01,
                             min_distance=20):
    my_cluster = [nucleon]
    my_center_x = sum(q.x for q in my_cluster) / len(my_cluster)
    my_center_y = sum(q.y for q in my_cluster) / len(my_cluster)

    for other in particles:
        if isinstance(other, Nucleon) and other.name == "H-1" and other not in my_cluster:
            other_cluster = [other]
            other_center_x = sum(q.x for q in other_cluster) / len(
                other_cluster)
            other_center_y = sum(q.y for q in other_cluster) / len(
                other_cluster)

            dx = other_center_x - my_center_x
            dy = other_center_y - my_center_y
            distance = math.hypot(dx, dy)

            if distance > 0:
                # Force magnitude inversely proportional to distance
                force = min(max_force, max_force * (min_distance / distance))
                # Direction normalized
                ax = (dx / distance) * force
                ay = (dy / distance) * force

                # Apply to entire cluster
                for q in my_cluster:
                    q.vx += ax
                    q.vy += ay
                # Optionally, pull the other cluster slightly back
                for q in other_cluster:
                    q.vx -= ax * 0.2
                    q.vy -= ay * 0.2


# ---------------- MERGING ----------------
def check_quarks_merging():
    quarks = [p for p in particles if isinstance(p, Quark)]

    for i in range(len(quarks)):
        cluster = []

        for j in range(len(quarks)):
            dx = quarks[i].x - quarks[j].x
            dy = quarks[i].y - quarks[j].y
            if math.hypot(dx, dy) < MERGE_DISTANCE:
                cluster.append(quarks[j])

        if len(cluster) >= 3:
            group = cluster[:3]

            if all(q.speed() < MERGE_SPEED_THRESHOLD for q in group):

                flavors = [q.flavor for q in group]

                if flavors.count("up") == 2 and flavors.count("down") == 1:
                    name = "H-1"
                elif flavors.count("down") == 2 and flavors.count("up") == 1:
                    name = "n"
                else:
                    continue

                avg_x = sum(q.x for q in group) / 3
                avg_y = sum(q.y for q in group) / 3

                particles.append(Nucleon(name,avg_x, avg_y))

                for q in group:
                    q.destroy = True

                # Spawn exactly three new quarks on merge
                for _ in range(3):
                    new_q = Quark()
                    new_q.x = random.uniform(-500, 500)
                    new_q.y = random.uniform(-500, 500)

                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 3)
                    new_q.vx = math.cos(angle) * speed
                    new_q.vy = math.sin(angle) * speed

                    particles.append(new_q)

                break

def check_atom_merging():
    atoms = [p for p in particles if isinstance(p, Atom)]

    for i in range(len(atoms)):
        cluster = []

        for j in range(len(atoms)):
            dx = atoms[i].x - atoms[j].x
            dy = atoms[i].y - atoms[j].y
            if math.hypot(dx, dy) < MERGE_DISTANCE+30:
                cluster.append(atoms[j])
        
        if len(cluster) == 2:
            group = cluster[:2]
           
            
            # Only consider merging if they are different types (proton vs neutron)
            name = Atom.merge(group[0], group[1])
            
            if(name != None):   
                if name in atoms:
                    print(name)
                    for q in group:
                        q.destroy = True
                    avg_x = sum(q.x for q in group) / len(group)
                    avg_y = sum(q.y for q in group) / len(group)
                    print("Merged atoms:", name)
                    particles.append(Atom(name, avg_x, avg_y, 10))
            
            break    

# ---------------- INIT ----------------
for _ in range(NUM_QUARKS):
    particles.append(Quark())

# ---------------- LOOP ----------------

running = True
while running:
    clock.tick(60)
    screen.fill((15, 15, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            gravity_active = True

        if event.type == pygame.MOUSEBUTTONUP:
            gravity_active = False

    if gravity_active:
        gravity_pos = pygame.mouse.get_pos()

    for p in particles:
        if p.destroy:
            particles.remove(p)
            continue
        p.update()

    handle_collisions()

    for p in particles:
        p.draw(screen)
        if isinstance(p, Nucleon) and p.name == "H-1":
            apply_cluster_attraction(p, particles)

    if gravity_active:
        mx, my = gravity_pos
        pygame.draw.circle(screen, (180, 180, 255), (mx, my), 25, 2)
        pygame.draw.circle(screen, (120, 120, 255), (mx, my), 10)

    check_quarks_merging()
    check_atom_merging()

    pygame.display.flip()

pygame.quit()