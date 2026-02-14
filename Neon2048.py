import pygame
import random
import sys

# Initialize Pygame FIRST
pygame.init()

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
SCREEN_WIDTH = GRID_WIDTH + 240
SCREEN_HEIGHT = GRID_HEIGHT + 120
FPS = 60

# Colors (particle-themed)
BG_COLOR = (20, 20, 40)  # Dark space
GRID_COLOR = (60, 60, 80)
EMPTY_COLOR = (40, 40, 60)

TILE_COLORS = {
    0: EMPTY_COLOR,
    2:    (255, 80, 80),    # Quark: red
    4:    (80, 255, 80),    # Proton: green
    8:    (40, 200, 40),    # Neutron: dark green
    16:   (80, 255, 255),   # Deuterium: cyan
    32:   (255, 255, 80),   # He: yellow
    64:   (255, 180, 80),   # C: orange
    128:  (80, 80, 255),    # O: blue
    256:  (200, 80, 255),   # Ne: purple
    512:  (255, 100, 200),  # Mg: pink
    1024: (150, 100, 255),  # Si: indigo
    2048: (255, 150, 50),   # Fe: gold-orange
}

FONT_COLOR_LIGHT = (255, 255, 255)
FONT_COLOR_DARK  = (20, 20, 40)

FONT_TITLE  = pygame.font.SysFont("arial", 48, bold=True)
FONT_SCORE  = pygame.font.SysFont("arial", 32, bold=True)
FONT_TILE   = pygame.font.SysFont("arial", 28, bold=True)
FONT_GAME_OVER = pygame.font.SysFont("arial", 50, bold=True)

# Particle labels (realistic fusion chain approximation)
TILE_LABELS = {
    2:    'q',
    4:    'p+',
    8:    'n',
    16:   '2H',
    32:   '4He',
    64:   '12C',
    128:  '16O',
    256:  '20Ne',
    512:  '24Mg',
    1024: '28Si',
    2048: '56Fe',
}

class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0  # Fusion energy
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = random.choices([2, 4], weights=[0.9, 0.1])[0]

    def can_move(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return True
                val = self.grid[r][c]
                if c < GRID_SIZE-1 and self.grid[r][c+1] == val: return True
                if r < GRID_SIZE-1 and self.grid[r+1][c] == val: return True
        return False

    def compress(self, row):
        new = [x for x in row if x != 0]
        i = 0
        while i < len(new)-1:
            if new[i] == new[i+1]:
                new[i] *= 2
                self.score += new[i]
                new.pop(i+1)
            else:
                i += 1
        new += [0] * (GRID_SIZE - len(new))
        return new

    def move_left(self):
        moved = False
        for r in range(GRID_SIZE):
            old = self.grid[r][:]
            self.grid[r] = self.compress(old)
            if self.grid[r] != old:
                moved = True
        return moved

    def move_right(self):
        moved = False
        for r in range(GRID_SIZE):
            old = self.grid[r][:]
            self.grid[r] = self.compress(old[::-1])[::-1]
            if self.grid[r] != old:
                moved = True
        return moved

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def transpose(self):
        self.grid = [list(col) for col in zip(*self.grid)]

    def move(self, direction):
        if self.game_over:
            return False
        moved = False
        if direction == "left":   moved = self.move_left()
        elif direction == "right": moved = self.move_right()
        elif direction == "up":    moved = self.move_up()
        elif direction == "down":  moved = self.move_down()
        if moved:
            self.add_random_tile()
            self.game_over = not self.can_move()
        return moved

def draw_grid(surface, game):
    surface.fill(BG_COLOR)

    # Draw tiles
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = game.grid[r][c]
            color = TILE_COLORS.get(value, (200, 200, 200))
            rect = pygame.Rect(c*CELL_SIZE + 10, r*CELL_SIZE + 90, CELL_SIZE - 20, CELL_SIZE - 20)
            pygame.draw.rect(surface, color, rect, border_radius=12)

            if value > 0:
                label = TILE_LABELS.get(value, str(value))
                text_color = FONT_COLOR_LIGHT if value >= 8 else FONT_COLOR_DARK
                text = FONT_TILE.render(label, True, text_color)
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

    # Grid lines
    for i in range(GRID_SIZE + 1):
        y = 90 + i * CELL_SIZE
        pygame.draw.line(surface, GRID_COLOR, (5, y), (GRID_WIDTH + 5, y), 8)
        x = 10 + i * CELL_SIZE
        pygame.draw.line(surface, GRID_COLOR, (x, 90), (x, 90 + GRID_HEIGHT), 8)

    # Sidebar
    title = FONT_TITLE.render("QUARK FUSION", True, (255, 255, 255))
    surface.blit(title, (GRID_WIDTH + 20, 30))

    score_label = FONT_SCORE.render("FUSION ENERGY", True, (150, 200, 255))
    score_val = FONT_SCORE.render(str(game.score), True, (255, 255, 100))
    surface.blit(score_label, (GRID_WIDTH + 20, 140))
    surface.blit(score_val, (GRID_WIDTH + 20, 180))

    # Instructions
    instr = pygame.font.SysFont("arial", 18).render("WASD / Arrows to slide & fuse", True, (100, 150, 200))
    surface.blit(instr, (GRID_WIDTH + 20, 250))

    if game.game_over:
        overlay = pygame.Surface((GRID_WIDTH + 20, GRID_HEIGHT + 20), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (-10, 80))

        go_text = FONT_GAME_OVER.render("BLACK HOLE!", True, (255, 100, 100))
        go_rect = go_text.get_rect(center=(GRID_WIDTH//2 + 10, 90 + GRID_HEIGHT//2))
        surface.blit(go_text, go_rect)

        restart_text = pygame.font.SysFont("arial", 24).render("R to restart", True, (200, 200, 255))
        surface.blit(restart_text, (GRID_WIDTH//2 - 50, 90 + GRID_HEIGHT//2 + 50))

def restart_game(game):
    game.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    game.score = 0
    game.game_over = False
    game.add_random_tile()
    game.add_random_tile()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Quark Fusion 2048 - Merge to Neon & Beyond!")
    clock = pygame.time.Clock()

    game = Game2048()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.game_over and event.key == pygame.K_r:
                    restart_game(game)
                elif not game.game_over:
                    moved = False
                    if event.key in (pygame.K_LEFT, pygame.K_a): moved = game.move("left")
                    elif event.key in (pygame.K_RIGHT, pygame.K_d): moved = game.move("right")
                    elif event.key in (pygame.K_UP, pygame.K_w): moved = game.move("up")
                    elif event.key in (pygame.K_DOWN, pygame.K_s): moved = game.move("down")

        draw_grid(screen, game)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()