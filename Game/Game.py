import pygame
import random
import math
from Constants import *
from Quark import Quark
from Nucleon import Nucleon
from Atom import Atom, atoms_symbols
from FusionCards import Discoveries, atoms_discovered

pygame.init()

pygame.mixer.init()
tone = pygame.mixer.Sound("100hz_tone.wav")
channel = None  # We'll use a specific channel to control the sound

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Sandbox - Up & Down Quarks")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

particles = []
popup = []
gravity_active = False
gravity_pos = (0, 0)

#camera information
camera_zoom = 1.0
ZOOM_MIN = 0.2
ZOOM_MAX = 5.0
ZOOM_STEP = 1.1
camera_x = WIDTH/2
camera_y = HEIGHT/2
camera_speed = 5


def clamp_camera():
    global camera_x, camera_y
    half_view_w = (WIDTH / 2) / camera_zoom
    half_view_h = (HEIGHT / 2) / camera_zoom

    if half_view_w >= WIDTH / 2:
        camera_x = WIDTH / 2
    else:
        camera_x = max(half_view_w, min(WIDTH - half_view_w, camera_x))

    if half_view_h >= HEIGHT / 2:
        camera_y = HEIGHT / 2
    else:
        camera_y = max(half_view_h, min(HEIGHT - half_view_h, camera_y))


def world_to_screen(pos):
    wx, wy = pos
    sx = (wx - camera_x) * camera_zoom + WIDTH / 2
    sy = (wy - camera_y) * camera_zoom + HEIGHT / 2
    return sx, sy


def \
        screen_to_world(pos):
    sx, sy = pos
    wx = (sx - WIDTH / 2) / camera_zoom + camera_x
    wy = (sy - HEIGHT / 2) / camera_zoom + camera_y
    return wx, wy


def zoom_at(screen_pos, zoom_factor):
    global camera_zoom, camera_x, camera_y
    if zoom_factor == 1.0:
        return
    before = screen_to_world(screen_pos)
    camera_zoom = max(ZOOM_MIN, min(ZOOM_MAX, camera_zoom * zoom_factor))
    camera_x = before[0] - (screen_pos[0] - WIDTH / 2) / camera_zoom
    camera_y = before[1] - (screen_pos[1] - HEIGHT / 2) / camera_zoom
    clamp_camera()

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

def apply_cluster_attraction(nucleon, particles, max_force=-0.01, min_distance=20):
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
                    new_q = Quark(random.choice(["up", "down"]))
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
            if math.hypot(dx, dy) < atoms[i].radius + atoms[j].radius + 30:
                cluster.append(atoms[j])
        
        if len(cluster) == 2:
            group = cluster[:2]

            # Only consider merging if they are different types (proton vs neutron)
            name = Atom.merge(group[0], group[1])
            
            print(name)
            if name != None and name in atoms_symbols:

                """for i in range(len(already_merged)):
                    if name == already_merged[i]:
                        # turn color of the grid into green
                        global discovered_counter
                        discovered_counter += 1
                        already_merged.remove(already_merged[i])"""

                print("Merged atoms:", name)
                avg_x = sum(q.x for q in group) / len(group)
                avg_y = sum(q.y for q in group) / len(group)
                print("Merged :", name)

                particles.append(Atom(name, avg_x, avg_y, 10))

                new_discovery = Discoveries(name)
                if atoms_discovered[atoms_symbols.index(name)] == False:
                    atoms_discovered[atoms_symbols.index(name)] = True
                    new_discovery.is_visible = True
                    popup.append(new_discovery)

                for q in group:
                    q.destroy = True
            
            break

@staticmethod
def add_atom(name, x, y, radius):
    if name in atoms_symbols:
        particles.append(Atom(name, x, y, radius))

@staticmethod
def remove_atom(atom):
    particles.remove(atom)

# ---------------- INIT ----------------
for _ in range(int(NUM_QUARKS/2)):
    particles.append(Quark("up"))
for _ in range(int(NUM_QUARKS / 2)):
    particles.append(Quark("down"))

# ---------------- LOOP ----------------

running = True
while running:
    clock.tick(60)
    screen.fill((15, 15, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Gravity well controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            gravity_active = True

        if event.type == pygame.MOUSEBUTTONUP:
            gravity_active = False

        # Camera Controls
        # Zoom in & out
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoom_at(pygame.mouse.get_pos(), ZOOM_STEP)
            elif event.y < 0:
                zoom_at(pygame.mouse.get_pos(), 1 / ZOOM_STEP)

        # Camera movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            camera_x -= camera_speed * camera_zoom
        if keys[pygame.K_d]:
            camera_x += camera_speed * camera_zoom
        if keys[pygame.K_w]:
            camera_y -= camera_speed * camera_zoom
        if keys[pygame.K_s]:
            camera_y += camera_speed * camera_zoom

        clamp_camera()

    if gravity_active:
        gravity_pos = screen_to_world(pygame.mouse.get_pos())

    # ---------Creates sound when hold mouse pad-----------

    mouse_buttons = pygame.mouse.get_pressed()

    if mouse_buttons[0]:  # If Left Mouse is held down
        if not pygame.mixer.get_busy():  # Only play if sound isn't already playing
            # -1 tells it to loop until we call stop()
            channel = tone.play(loops=-1)
    else:
        # If the mouse is released, stop the sound
        tone.fadeout(2000)
        '''if channel:
            channel.stop()'''

    for p in particles:
        if p.destroy:
            particles.remove(p)
            continue
        p.update()

    for popups in popup:
        popups.handle_event(event)

    handle_collisions()

    for p in particles:
        p.draw(screen)
        # if isinstance(p, Nucleon) and p.name == "H-1":
            # apply_cluster_attraction(p, particles)

    for popups in popup:
        popups.draw(screen)

    if gravity_active:
        mx, my = world_to_screen(gravity_pos)
        outer_radius = max(1, int(25 * camera_zoom))
        inner_radius = max(1, int(10 * camera_zoom))
        pygame.draw.circle(screen, (180, 180, 255), (int(mx), int(my)), outer_radius, 2)
        pygame.draw.circle(screen, (120, 120, 255), (int(mx), int(my)), inner_radius)

    check_quarks_merging()
    check_atom_merging()

    pygame.display.flip()

pygame.quit()