import pygame
from Atom import *
import radioactivedecay as rd
from Constants import *


atoms_info = [
    "The lightest of all quarks; it makes protons stable.",
    "Slightly heavier than the Up quark; it helps make neutrons.",
    "Free neutrons decay in about 15 minutes, but are stable in atoms.",
    "The most abundant atom in the universe (99.98% of hydrogen).",
    "Also called Deuterium; it is stable and used in nuclear fusion.",
    "Also called Tritium; it is radioactive and makes watch hands glow.",
    "Extremely rare on Earth but abundant on the Moon; a potential future fuel.",
    "An Alpha particle! It makes balloons float and voices squeaky.",
    "Used in lithium-ion batteries and to breed tritium for fusion.",
    "Created in the Big Bang; it makes up 92% of all lithium.",
    "It decays by 'eating' one of its own electrons (electron capture).",
    "It is great at absorbing neutrons, so it is used in nuclear control rods.",
    "A rare isotope found in ice cores that helps track solar activity.",
    "It is transparent to neutrons and makes up 80% of natural boron.",
    "A very short-lived isotope that turns into Boron in just 19 seconds.",
    "Used in PET scans to visualize the human brain.",
    "Used in heart imaging to measure blood flow.",
    "A rare, short-lived oxygen that helps power stars in the CNO cycle.",
    "The standard! One 'atomic mass unit' is defined as 1/12th of this atom.",
    "Unlike C-12, this carbon is magnetic and used in chemical analysis (NMR).",
    "Radiocarbon! It is used to date ancient artifacts and fossils.",
    "The main ingredient of Earth's atmosphere (about 99.6% of nitrogen).",
    "Stable and rare, it is used as a tracer in biology and to study proteins with NMR.",
    "A 'double magic' nucleus, making it incredibly stable and abundant.",
    "Used in medical scans to measure oxygen use in the brain.",
    "A rare, heavy oxygen used to study how plants use water.",
    "Climate thermometer! Its ratio in ice tells us about ancient temperatures.",
    "The only stable isotope of fluorine; essentially 100% of natural fluorine.",
    "The superstar of medical imaging; used to detect cancer in FDG-PET scans.",
    "The first isotope ever discovered (in 1913); it glows red-orange in signs."
]
atoms_discovered = [False] * 30

class Popup:
    def __init__(self, x, y, width, height, title, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)  # Light Gray
        self.title = title
        self.text = text
        self.is_visible = False
        self.line_spacing = 30
        self.padding = 15
        self.color = color
        self.body_color = (30, 30, 45)
        self.header_height = 40
        self.exit_button = pygame.Rect(self.rect.x + self.header_height / 4,
                                       self.rect.y + self.header_height / 4,
                                       20, 20)

        self.title_font = pygame.font.SysFont(TITLE_FONT, TITLE_FONT_SIZE, bold=True)
        self.font = pygame.font.SysFont(TEXT_FONT, TEXT_FONT_SIZE)

    def get_wrapped_lines(self):
        words = self.text.split(' ')
        lines = []
        current_line = ""
        max_text_width = self.rect.width - (self.padding * 2)

        for word in words:
            # Check if adding the next word exceeds the width
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_text_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)  # Add the final line
        return lines

    def draw(self, screen):
        if self.is_visible:
            # Shadow effect
            shadow_offset = 7
            shadow_rect = self.rect.move(shadow_offset, shadow_offset)
            pygame.draw.rect(screen, self.color, shadow_rect, border_radius=15)
            pygame.draw.rect(screen, self.color, (self.rect.x + shadow_offset,
                                                  self.rect.y + shadow_offset,
                                                  self.rect.width,
                                                  self.header_height))

            # Main Box
            pygame.draw.rect(screen, self.body_color, self.rect,
                             border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2,
                             border_radius=15)  # Border

            # Render Wrapped Text
            lines = self.get_wrapped_lines()
            for i, line in enumerate(lines):
                line_surf = self.font.render(line.strip(), True,
                                             (255, 255, 255))
                # Position each line based on its index
                line_y = self.rect.y + self.header_height + self.padding + (
                            i * self.line_spacing)

                # Check to make sure we don't draw outside the box bottom
                if line_y < self.rect.bottom - self.padding:
                    screen.blit(line_surf,
                                (self.rect.x + self.padding, line_y))

            # Title box

            header_rect = pygame.Rect(self.rect.x, self.rect.y,
                                      self.rect.width, self.header_height)
            pygame.draw.rect(screen, self.color, header_rect)
            pygame.draw.line(screen, (255, 255, 255),
                             (self.rect.x, self.rect.y + self.header_height),
                             (self.rect.right - 1,
                              self.rect.y + self.header_height), 2)

            # Title text
            title_surf = self.title_font.render(self.title, True, (0, 0, 0))
            title_rect = title_surf.get_rect(center=header_rect.center)
            screen.blit(title_surf, title_rect)

            # exit button
            pygame.draw.rect(screen, (0, 0, 0), self.exit_button)
            # Line 1: Top-left to bottom-right
            x_margin = 5
            pygame.draw.line(screen, (255, 255, 255),
                             (self.exit_button.x + x_margin,
                              self.exit_button.y + x_margin),
                             (self.exit_button.right - x_margin,
                              self.exit_button.bottom - x_margin), 3)
            # Line 2: Top-right to bottom-left
            pygame.draw.line(screen, (255, 255, 255),
                             (self.exit_button.right - x_margin,
                              self.exit_button.y + x_margin),
                             (self.exit_button.x + x_margin,
                              self.exit_button.bottom - x_margin), 3)

    def toggle(self):
        self.is_visible = not self.is_visible

    def handle_exit(self, event):
        if self.is_visible and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click only
                # Check if the click position is inside your exit_square
                if self.exit_button.collidepoint(event.pos):
                    self.is_visible = False


class Discoveries(Popup):
    def __init__(self, element, x=None, y=None):
        index = atoms_symbols.index(element)
        WIDTH = 400
        HEIGHT = 250
        if x == None and y == None:
            super().__init__((WIDTH * 2.4), (HEIGHT * 0.2), WIDTH, HEIGHT,
                            atoms_name[index], atoms_info[index],
                            atoms_color[index])
        else: 
            super().__init__(x, y, WIDTH, HEIGHT,
                            atoms_name[index], atoms_info[index],
                            atoms_color[index]) 







