import pygame
import pygame.freetype
import os
from gui.config import WINDOW_SIZE


class LevelPage:
    def __init__(self, level):
        self.level = level
        self.files = self.get_files()
        self.selected_file = None
        self.dropdown_active = False
        self.animation_speed = 0.5  # Speed of the dropdown animation
        self.hovered_index = -1  # Index of the hovered item
        self.scroll_offset = 0  # To track the scrolling position
        self.max_visible_items = 5  # Maximum number of items visible in the dropdown at a time

        # Load background image
        self.background = pygame.image.load("assets/images/Menu/background.png")
        self.background = pygame.transform.scale(self.background, WINDOW_SIZE)

        # Dropdown configuration
        self.font = pygame.freetype.Font("assets/images/Menu/amongus.ttf", 30)  # Load custom font
        self.dropdown_rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 - 150,
            WINDOW_SIZE[1] / 3 + 15,
            300,
            50
        )  # Centered dropdown
        self.dropdown_height = 0
        self.max_height = 50 * min(self.max_visible_items, len(self.files))  # Calculate max height based on number of items

    def get_files(self):
        folder = f"assets/JSON/"
        print(f"Getting files from {folder}")
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        files.sort()
        return files

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Common arrow settings
        arrow_color = (0, 0, 0)
        arrow_size = 20

        # Draw dropdown background for file selection
        pygame.draw.rect(screen, (255, 255, 255), self.dropdown_rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.dropdown_rect, 2)

        # Draw the selected file or placeholder
        if self.selected_file:
            self.font.render_to(screen, (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10), self.selected_file, (0, 0, 0))
        else:
            self.font.render_to(screen, (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10), "Select a file", (0, 0, 0))

        # Draw arrow for file dropdown
        arrow_pos = (self.dropdown_rect.x + self.dropdown_rect.width - 30, self.dropdown_rect.y + 10)

        if self.dropdown_active:
            pygame.draw.polygon(screen, arrow_color, [(arrow_pos[0], arrow_pos[1]), (arrow_pos[0] + arrow_size, arrow_pos[1] + arrow_size), (arrow_pos[0] - arrow_size, arrow_pos[1] + arrow_size)])
        else:
            pygame.draw.polygon(screen, arrow_color, [(arrow_pos[0], arrow_pos[1] + arrow_size), (arrow_pos[0] + arrow_size, arrow_pos[1]), (arrow_pos[0] - arrow_size, arrow_pos[1])])

        # Update dropdown height for file selection
        if self.dropdown_active:
            self.dropdown_height = min(self.dropdown_height + self.animation_speed * 5, self.max_height)
        else:
            self.dropdown_height = max(self.dropdown_height - self.animation_speed * 5, 0)

        # Draw file dropdown options with animation and scrolling
        if self.dropdown_height > 0:
            visible_files = self.files[self.scroll_offset:self.scroll_offset + self.max_visible_items]
            num_items_visible = int(self.dropdown_height / 50)
            for i in range(min(num_items_visible, len(visible_files))):
                file = visible_files[i]

                offset = 50 * (i + 1)
                if i == num_items_visible - 1:
                    offset = self.dropdown_height
                if i > num_items_visible - 1:
                    break
                item_rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + offset, self.dropdown_rect.width, 50)

                # Change color on hover
                item_color = (200, 200, 200) if i + self.scroll_offset == self.hovered_index else (255, 255, 255)
                pygame.draw.rect(screen, item_color, item_rect, 0)
                pygame.draw.rect(screen, (0, 0, 0), item_rect, 2)

                # Render the file name
                self.font.render_to(screen, (item_rect.x + 10, item_rect.y + 10), file, (0, 0, 0))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.dropdown_rect.collidepoint(mouse_pos):
                    self.dropdown_active = not self.dropdown_active
                elif self.dropdown_active:
                    for i, file in enumerate(self.files[self.scroll_offset:self.scroll_offset + self.max_visible_items]):
                        rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + 50 * (i + 1), self.dropdown_rect.width, 50)
                        if rect.collidepoint(mouse_pos):
                            self.selected_file = file
                            self.dropdown_active = False
                            return f"{file}"
            elif event.type == pygame.MOUSEWHEEL:
                if self.dropdown_active:
                    self.handle_scroll(event.y)
                    # Prevent further processing if scrolling
                    return None

        return None

    def handle_mouse_motion(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.dropdown_active:
            for i in range(len(self.files[self.scroll_offset:self.scroll_offset + self.max_visible_items])):
                rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + 50 * (i + 1), self.dropdown_rect.width, 50)
                if rect.collidepoint(mouse_pos):
                    self.hovered_index = i + self.scroll_offset
                    break
            else:
                self.hovered_index = -1

    def handle_scroll(self, scroll_direction):
        if scroll_direction > 0:  # Scroll up
            self.scroll_offset = max(0, self.scroll_offset - 1)
        elif scroll_direction < 0:  # Scroll down
            if self.scroll_offset + self.max_visible_items < len(self.files):
                self.scroll_offset += 1
