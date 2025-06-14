import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class DropDown:
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, border_radius=6)
        msg = self.font.render(self.main, True, BLACK)
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, border_radius=6)
                msg = self.font.render(text, True, BLACK)
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        self.active_option = -1

        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1

def select_algorithm(screen):
    clock = pygame.time.Clock()

    # Dynamically scaled sizes
    box_width = int(SCREEN_WIDTH * 0.40)
    box_height = int(SCREEN_HEIGHT * 0.10)
    spacing_between = int(SCREEN_WIDTH * 0.05)
    dropdown_y = int(SCREEN_HEIGHT * 0.25)

    # Font Scaling
    medium_font_size = min(int(SCREEN_HEIGHT * 0.04), 32)
    large_font_size = int(SCREEN_HEIGHT * 0.05)
    dynamic_font = pygame.font.SysFont("Arial", medium_font_size)
    large_font = pygame.font.SysFont("Arial", large_font_size, bold=True)

    # Vertical placement
    header_y = int(SCREEN_HEIGHT * 0.08)
    label_y = int(SCREEN_HEIGHT * 0.22)
    dropdown_y = int(SCREEN_HEIGHT * 0.32)

    total_width = box_width * 2 + spacing_between
    start_x = (SCREEN_WIDTH - total_width) // 2

    gen_x = start_x
    solve_x = start_x + box_width + spacing_between

    COLOR_INACTIVE = (180, 180, 255)
    COLOR_ACTIVE = (100, 200, 255)
    COLOR_LIST_INACTIVE = (220, 220, 220)
    COLOR_LIST_ACTIVE = (180, 255, 180)

    dropdown_gen = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        gen_x, dropdown_y, box_width, box_height, dynamic_font,
        "Select Generator", ["DFS", "Prim's", "Kruskal", "Hunt-and-Kill"]
    )

    dropdown_solve = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        solve_x, dropdown_y, box_width, box_height, dynamic_font,
        "Select Solver", ["DFS", "BFS", "A-Star", "Dijkstra"]
    )

    # Start button setup
    button_width = int(SCREEN_WIDTH * 0.25)
    button_height = int(SCREEN_HEIGHT * 0.10)
    button_y = dropdown_y + box_height * 5.4
    button_x = (gen_x + solve_x + box_width) // 2 - button_width // 2

    start_button = pygame.Rect(button_x, button_y, button_width, button_height)

    selecting = True
    gen_index = 0
    solve_index = 0

    while selecting:
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                selecting = False

        selected_gen = dropdown_gen.update(event_list)
        if selected_gen >= 0:
            dropdown_gen.main = dropdown_gen.options[selected_gen]
            gen_index = selected_gen

        selected_solve = dropdown_solve.update(event_list)
        if selected_solve >= 0:
            dropdown_solve.main = dropdown_solve.options[selected_solve]
            solve_index = selected_solve

        screen.fill(WHITE)

        # Main Title
        title = large_font.render("Maze Configuration", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, header_y))

        # Section Labels (now in large font too)
        gen_label = large_font.render("Maze Generator", True, BLACK)
        solve_label = large_font.render("Maze Solver", True, BLACK)
        screen.blit(gen_label, (gen_x + box_width // 2 - gen_label.get_width() // 2, label_y))
        screen.blit(solve_label, (solve_x + box_width // 2 - solve_label.get_width() // 2, label_y))

        # Draw dropdowns
        dropdown_gen.draw(screen)
        dropdown_solve.draw(screen)

        # Draw start button
        pygame.draw.rect(screen, (50, 150, 100), start_button, border_radius=10)
        start_text = dynamic_font.render("START", True, WHITE)
        screen.blit(start_text, start_text.get_rect(center=start_button.center))

        pygame.display.flip()
        clock.tick(30)

    return dropdown_gen.options[gen_index].lower(), dropdown_solve.options[solve_index].lower()
