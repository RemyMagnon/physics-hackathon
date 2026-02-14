import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Billiards")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# --- Game Variables ---
particles = []
spawn_interval = 5000  # milliseconds
last_spawn_time = pygame.time.get_ticks()

offset = 8  # distance between quarks in a pair

# Mouse dragging
dragging = False
drag_start = (0, 0)
DRAG_COOLDOWN = 3000  # milliseconds
last_drag_time = -DRAG_COOLDOWN
# --- Box Settings ---
BOX_X, BOX_Y = 150, 125
BOX_WIDTH, BOX_HEIGHT = 700, 600
BOX_COLOR = (50, 50, 50)

# --- Tunnel Settings ---
TUNNEL_WIDTH = 200
TUNNEL_HEIGHT = 100
TUNNEL_X = BOX_X - TUNNEL_WIDTH - 5  # left of box
TUNNEL_Y = BOX_Y + BOX_HEIGHT // 2 - TUNNEL_HEIGHT // 2
TUNNEL_COLOR = (200, 200, 50)
PROTON_SPEED = 3
PROTON_SPAWN_INTERVAL = 7000  # ms
PROTON_SPAWN_LOCATION_X = TUNNEL_X + TUNNEL_WIDTH + 5
PROTON_SPAWN_LOCATION_Y = TUNNEL_Y + TUNNEL_HEIGHT / 2

last_proton_spawn = pygame.time.get_ticks()


def spawn_new_quark(x, y):
    # 1/4 chance to spawn a pair, 3/4 chance to spawn a single
    choice = random.choice(['pair', 'single', 'single', 'single'])
    if choice == 'pair':
        q1 = Quark(x - offset / 2, y)
        q2 = Quark(x + offset / 2, y)
        # Make them neighbours so they stick
        q1.neighbour = q2
        q2.neighbour = q1
        particles.append(q1)
        particles.append(q2)
    elif choice == 'single':
        particles.append(Quark(x, y))


def stick_particles(p1, p2, target_distance=8):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.hypot(dx, dy)

    if distance == 0:
        return  # avoid division by zero

    diff = (distance - target_distance) / distance
    adjust_x = dx * 0.5 * diff
    adjust_y = dy * 0.5 * diff

    p1.x += adjust_x
    p1.y += adjust_y
    p2.x -= adjust_x
    p2.y -= adjust_y


def cluster_center(quark):
    cluster = [quark] + quark.neighbours
    x = sum(q.x for q in cluster) / len(cluster)
    y = sum(q.y for q in cluster) / len(cluster)
    return x, y


"""
    Apply subtle attraction to other clusters based on distance.
    max_force: max acceleration applied per frame
    min_distance: distance below which force is capped
"""


def apply_cluster_attraction(quark, particles, max_force=0.05,
                             min_distance=20):
    my_cluster = [quark] + quark.neighbours
    my_center_x = sum(q.x for q in my_cluster) / len(my_cluster)
    my_center_y = sum(q.y for q in my_cluster) / len(my_cluster)

    for other in particles:
        if isinstance(other, Quark) and other not in my_cluster:
            other_cluster = [other] + other.neighbours
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
                    q.vx -= ax * 0.3
                    q.vy -= ay * 0.3


def check_for_nucleon_formation():
    for p in particles:
        if isinstance(p, Quark):
            cluster = [p] + p.neighbours
            if len(cluster) == 3 and not any(q.destroy for q in cluster):
                # Remove quarks from particles list
                for q in cluster:
                    if q in particles:
                        q.destroy = True
                # Create nucleon
                avg_x = sum(q.x for q in cluster) / 3
                avg_y = sum(q.y for q in cluster) / 3
                avg_vx = sum(q.vx for q in cluster) / 3
                avg_vy = sum(q.vy for q in cluster) / 3

                nucleon = Nucleon(avg_x, avg_y, avg_vx, avg_vy)
                particles.append(nucleon)


class Particle:
    def __init__(self, x=None, y=None, vx=None, vy=None, radius=5):
        self.radius = radius
        self.x = x if x is not None else random.randint(radius, WIDTH - radius)
        self.y = y if y is not None else random.randint(radius,
                                                        HEIGHT - radius)
        self.vx = vx if vx is not None else 0
        self.vy = vy if vy is not None else 0
        self.neighbour = None  # particle this one is "stuck" to
        self.destroy = False  # for particles that need to be removed

    def update(self):
        # Move normally
        self.x += self.vx
        self.y += self.vy

        # Stick to neighbour if any
        if self.neighbour is not None:
            stick_particles(self, self.neighbour)

    def draw(self, surface):
        pass  # to be implemented in subclasses


# --- Quark Class ---
class Quark(Particle):
    MAX_CLUSTER_SIZE = 3

    def __init__(self, x=None, y=None, vx=None, vy=None):
        if vx is None or vy is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = 0.3
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
        super().__init__(x, y, vx, vy, radius=5)
        self.neighbours = []  # list of other quarks in cluster

    def update(self):
        # Move
        self.x += self.vx
        self.y += self.vy

        # Bounce inside box
        if self.x - self.radius <= BOX_X:
            self.x = BOX_X + self.radius
            self.vx *= -random.uniform(0.9, 1.1)
        if self.x + self.radius >= BOX_X + BOX_WIDTH:
            self.x = BOX_X + BOX_WIDTH - self.radius
            self.vx *= -random.uniform(0.9, 1.1)
        if self.y - self.radius <= BOX_Y:
            self.y = BOX_Y + self.radius
            self.vy *= -random.uniform(0.9, 1.1)
        if self.y + self.radius >= BOX_Y + BOX_HEIGHT:
            self.y = BOX_Y + BOX_HEIGHT - self.radius
            self.vy *= -random.uniform(0.9, 1.1)

        # Stick to neighbours
        for n in self.neighbours:
            stick_particles(self, n)

    def draw(self, surface):

        for n in self.neighbours:
            pygame.draw.line(surface, (255, 200, 200), (self.x, self.y),
                             (n.x, n.y), 2)

        pygame.draw.circle(surface, (255, 80, 80), (int(self.x), int(self.y)),
                           self.radius)
        text = font.render("Q", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)

        apply_cluster_attraction(self, particles, max_force=0.02,
                                 min_distance=50)

    def try_stick(self, other):
        # Build clusters for self and other
        cluster1 = [self] + self.neighbours
        cluster2 = [other] + getattr(other, 'neighbours', [])

        # If combined size exceeds max, don't stick
        if len(cluster1) + len(cluster2) > self.MAX_CLUSTER_SIZE:
            return

        # Merge clusters
        new_cluster = []
        for q in cluster1 + cluster2:
            if q not in new_cluster:
                new_cluster.append(q)

        # Update neighbours for all
        for q in new_cluster:
            q.neighbours = [other_q for other_q in new_cluster if other_q != q]

    def check_collision_with_other_quarks(self, particle_list):
        for other in particle_list:
            if isinstance(other, Quark) and other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.hypot(dx, dy)
                if distance < self.radius + other.radius:
                    self.try_stick(other)


class Proton(Particle):
    def __init__(self, x=None, y=None, vx=None, vy=None):
        if vx is None or vy is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = 2
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
        super().__init__(x, y, vx, vy, radius=15)

    def draw(self, surface):
        pygame.draw.circle(surface, (80, 255, 80), (int(self.x), int(self.y)),
                           self.radius)
        text = font.render("P", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)

    def check_collision_with_other_protons(self, particle_list):
        for other in particle_list:
            if other != self and isinstance(other,
                                            Proton) and not other.destroy:
                dx = self.x - other.x
                dy = self.y - other.y
                distance = math.hypot(dx, dy)
                if distance < self.radius + other.radius:
                    # Collision detected, destroy both
                    self.destroy = True
                    other.destroy = True
                    # Spawn a new quark pair
                    spawn_new_quark((self.x + other.x) / 2,
                                    (self.y + other.y) / 2)
                    break  # stop after collision


# Nucleon is a cluster of 3 quarks that moves as one particle
class Nucleon:
    def __init__(self, x, y, vx, vy):
        self.radius = 12  # visual size of the nucleon
        # Compute center of mass
        self.x = x
        self.y = y
        # Compute average velocity to preserve momentum
        self.vx = vx
        self.vy = vy
        self.destroy = False

    def update(self):
        # Move as one particle
        self.x += self.vx
        self.y += self.vy

        # Bounce inside box
        if self.x - self.radius <= BOX_X:
            self.x = BOX_X + self.radius
            self.vx *= -0.9
        if self.x + self.radius >= BOX_X + BOX_WIDTH:
            self.x = BOX_X + BOX_WIDTH - self.radius
            self.vx *= -0.9
        if self.y - self.radius <= BOX_Y:
            self.y = BOX_Y + self.radius
            self.vy *= -0.9
        if self.y + self.radius >= BOX_Y + BOX_HEIGHT:
            self.y = BOX_Y + BOX_HEIGHT - self.radius
            self.vy *= -0.9

    def draw(self, surface):
        # Draw nucleon as a circle
        pygame.draw.circle(surface, (80, 120, 255), (int(self.x), int(self.y)),
                           self.radius)
    # text = font.render("N", True, (255, 255, 255))
    # text_rect = text.get_rect(center=(self.x, self.y))
    # surface.blit(text, text_rect)


# Initial proton

particles.append(Proton())

running = True
while running:
    clock.tick(60)
    screen.fill((20, 20, 40))  # pool table green

    pygame.draw.rect(screen, BOX_COLOR, (BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT),
                     3)

    # Draw tunnel
    pygame.draw.rect(screen, TUNNEL_COLOR,
                     (TUNNEL_X, TUNNEL_Y, TUNNEL_WIDTH, TUNNEL_HEIGHT))

    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse drag start
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # cool time setting
            if current_time - last_drag_time >= DRAG_COOLDOWN:
                if not (BOX_X <= mouse_pos[0] <= BOX_X + BOX_WIDTH and BOX_Y <=
                        mouse_pos[1] <= BOX_Y + BOX_HEIGHT):
                    dragging = True
                    drag_start = mouse_pos

        # Mouse drag end
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                drag_end = pygame.mouse.get_pos()
                dx = drag_end[0] - drag_start[0]
                dy = drag_end[1] - drag_start[1]

                # Reverse direction and scale
                scale = 0.1  # adjust speed
                vx = -dx * scale
                vy = -dy * scale

                particles.append(
                    Proton(x=drag_end[0], y=drag_end[1], vx=vx, vy=vy))
                dragging = False
                last_drag_time = pygame.time.get_ticks()  # reset cooldown

    # Spawn every 7 seconds
    if current_time - last_proton_spawn > PROTON_SPAWN_INTERVAL:
        vx = random.uniform(0, PROTON_SPEED)
        vy = random.uniform(-PROTON_SPEED / 2, PROTON_SPEED / 2)
        particles.append(
            Proton(x=PROTON_SPAWN_LOCATION_X, y=PROTON_SPAWN_LOCATION_Y, vx=vx,
                   vy=vy))
        last_proton_spawn = current_time

    # Remove destroyed

    # Update
    for p in particles:
        if p.destroy:
            particles.remove(p)
            continue
        p.update()
        # Collisions
        if isinstance(p, Proton):
            p.check_collision_with_other_protons(particles)
        if isinstance(p, Quark):
            p.check_collision_with_other_quarks(particles)

        p.draw(screen)

    check_for_nucleon_formation()

    # Draw drag line
    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 0), drag_start, mouse_pos, 2)

    pygame.display.flip()

pygame.quit()