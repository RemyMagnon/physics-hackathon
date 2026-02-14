import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Sandbox - Up & Down Quarks")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

# ----------- PARAMETERS -----------
NUM_QUARKS = 10
QUARK_RADIUS = 8
NUCLEON_RADIUS = 12
ATOM_RADIUS = 20

GRAVITY_STRENGTH = 40
MERGE_DISTANCE = 30
MERGE_SPEED_THRESHOLD = 12
# ----------------------------------

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
            if hasattr(particles[i], 'radius') and hasattr(particles[j], 'radius'):
                resolve_collision(particles[i], particles[j])

# ---------------- CLASSES ----------------
class Quark:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0, 1)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = QUARK_RADIUS
        self.destroy = False
        self.flavor = random.choice(["up", "down"])

    def update(self):
        if gravity_active:
            dx = gravity_pos[0] - self.x
            dy = gravity_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                force = GRAVITY_STRENGTH / (dist * dist)
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force

        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def draw(self, surface):
        color = (255, 100, 100) if self.flavor == "up" else (100, 150, 255)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        label = "u" if self.flavor == "up" else "d"
        text = font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)

class Nucleon:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.radius = NUCLEON_RADIUS
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.destroy = False

    def update(self):
        if gravity_active:
            dx = gravity_pos[0] - self.x
            dy = gravity_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                force = (GRAVITY_STRENGTH * 0.6) / (dist * dist)
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force

        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, surface):
        color = (255, 80, 80) if self.kind == "proton" else (80, 140, 255)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        label = "P" if self.kind == "proton" else "N"
        text = font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)

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
        if gravity_active:
            dx = gravity_pos[0] - self.x
            dy = gravity_pos[1] - self.y
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
        pygame.draw.circle(surface, (255, 255, 100), (int(self.x), int(self.y)), self.radius)
        text = font.render("e", True, (0, 0, 0))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)

class Atom:
    def __init__(self, x, y, nucleons, electrons):
        self.x = x
        self.y = y
        self.nucleons = nucleons
        self.electrons = electrons
        self.radius = ATOM_RADIUS
        self.vx = sum(n.vx for n in nucleons)/len(nucleons)
        self.vy = sum(n.vy for n in nucleons)/len(nucleons)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH
        self.y %= HEIGHT

        # Move nucleons and electrons with atom
        for n in self.nucleons:
            n.x = self.x + (n.x - self.x)
            n.y = self.y + (n.y - self.y)
        for e in self.electrons:
            e.x = self.x + (e.x - self.x)
            e.y = self.y + (e.y - self.y)

    def draw(self, surface):
        pygame.draw.circle(surface, (100, 255, 100), (int(self.x), int(self.y)), self.radius, 2)
        for n in self.nucleons:
            n.draw(surface)
        for e in self.electrons:
            e.draw(surface)
        label = f"H" if len(self.nucleons) == 1 else f"He" if len(self.nucleons) == 4 else "Atom"
        text = font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)

# ---------------- MERGING ----------------
def check_quark_merging():
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
                    kind = "proton"
                elif flavors.count("down") == 2 and flavors.count("up") == 1:
                    kind = "neutron"
                else:
                    continue
                avg_x = sum(q.x for q in group) / 3
                avg_y = sum(q.y for q in group) / 3
                particles.append(Nucleon(avg_x, avg_y, kind))
                for q in group:
                    q.destroy = True
                # Spawn exactly three new quarks
                for _ in range(3):
                    new_q = Quark()
                    new_q.x = random.uniform(-500, 500)
                    new_q.y = random.uniform(-500, 500)
                    angle = random.uniform(0, 2*math.pi)
                    speed = random.uniform(1, 3)
                    new_q.vx = math.cos(angle)*speed
                    new_q.vy = math.sin(angle)*speed
                    particles.append(new_q)
                break

def check_atom_merging():
    nucleons = [p for p in particles if isinstance(p, Nucleon)]
    electrons = [p for p in particles if isinstance(p, Electron)]
    for n in nucleons:
        nearby_e = [e for e in electrons if math.hypot(e.x - n.x, e.y - n.y) < MERGE_DISTANCE]
        if nearby_e:
            e = nearby_e[0]
            atom = Atom(n.x, n.y, [n], [e])
            particles.append(atom)
            n.destroy = True
            e.destroy = True

# ---------------- INIT ----------------
for _ in range(NUM_QUARKS):
    particles.append(Quark())
for _ in range(NUM_QUARKS):
    particles.append(Electron())

# ---------------- MAIN LOOP ----------------
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

    for p in particles[:]:
        if hasattr(p, "destroy") and p.destroy:
            particles.remove(p)
            continue
        p.update()

    handle_collisions()

    for p in particles:
        p.draw(screen)

    if gravity_active:
        mx, my = gravity_pos
        pygame.draw.circle(screen, (180, 180, 255), (mx, my), 25, 2)
        pygame.draw.circle(screen, (120, 120, 255), (mx, my), 10)

    check_quark_merging()
    check_atom_merging()

    pygame.display.flip()

pygame.quit()
