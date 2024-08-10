import pygame
import os
from gui.config import *

class Sidebar:
    def __init__(self, buttons, logs, offset=(0, 0), on_previous=None, on_next=None, on_play_stop=None):
        self.buttons = buttons
        self.logs = logs
        self.offset = offset
        self.load_button_images()
        self.current_log_index = 0  # Index to track the current starting line
        self.lines_per_page = 15  # Number of lines that fit in the display area
        self.on_previous = on_previous  # Callback for previous button
        self.on_next = on_next  # Callback for next button
        self.on_play_stop = on_play_stop  # Callback for play/stop button

    def load_button_images(self):
        self.button_images = {
            "previous": pygame.image.load(
                os.path.join(CONTROLBUTTON_FOLDER, "prev.png")
            ),
            "next": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "next.png")),
            "play": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "play.png")),
            "pause": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "pause.png")),
            "up": pygame.image.load((CONTROLBUTTON_FOLDER + "/up.png")),  # New Up button image
            "down": pygame.image.load((CONTROLBUTTON_FOLDER + "/down.png")),  # New Down button image
        }
        for key in self.button_images:
            self.button_images[key] = pygame.transform.scale(
                self.button_images[key], (30, 30)  # Smaller, more subtle buttons
            )

    def draw(self, screen, current_turn):
        sidebar_bg_color = (50, 50, 50)  # Darker gray for a modern look
        sidebar_x = WINDOW_SIZE[0] - SIDEBAR_WIDTH + self.offset[0]
        sidebar_y = self.offset[1]
        sidebar_width = SIDEBAR_WIDTH
        sidebar_height = WINDOW_SIZE[1]

        # Draw sidebar background
        pygame.draw.rect(
            screen,
            sidebar_bg_color,
            (sidebar_x, sidebar_y, sidebar_width, sidebar_height),
        )

        # Draw sidebar border
        pygame.draw.rect(
            screen, (30, 30, 30), (sidebar_x, sidebar_y, sidebar_width, sidebar_height), 2
        )

        # Section 1: Player Properties (using the latest log)
        latest_log = self.logs[current_turn]
        self.draw_player_properties(screen, sidebar_x, sidebar_y, latest_log)

        # Section 2: Scrollable Log
        log_area_top = sidebar_y + 280
        self.draw_scrollable_log(screen, sidebar_x, log_area_top, sidebar_width, current_turn)

        # Section 3: Control Buttons
        button_area_top = sidebar_height - 80
        self.draw_control_buttons(screen, sidebar_x, button_area_top)

    def draw_player_properties(self, screen, sidebar_x, sidebar_y, data):
        font = pygame.font.Font(None, 24)
        title_font = pygame.font.Font(None, 30)

        # Title
        title_text = title_font.render("Player Stats", True, (255, 255, 255))
        screen.blit(title_text, (sidebar_x + 10, sidebar_y + 10))

        # Properties
        sidebar_line_height = 30
        sidebar_margin_top = 40
        sidebar_margin_left = sidebar_x + 10

        player_properties = [
            f"Turn: {data['turn']}",
            f"Direction: {data['direction']}",
            f"Health: {data['health']}",
            f"Score: {data['score']}",
            f"Potion: {data['potion']}",
            f"Action: {data['action']}",
            f"Position: ({data['position'][0]}, {data['position'][1]})",
        ]

        for i, prop in enumerate(player_properties):
            prop_text = font.render(prop, True, (200, 200, 200))
            screen.blit(
                prop_text,
                (sidebar_margin_left, sidebar_y + sidebar_margin_top + i * sidebar_line_height),
            )

    def draw_scrollable_log(self, screen, sidebar_x, log_area_top, sidebar_width, current_turn):
        log_area_rect = pygame.Rect(sidebar_x + 10, log_area_top, sidebar_width - 20, 300)
        pygame.draw.rect(screen, (40, 40, 40), log_area_rect)

        font = pygame.font.Font(None, 20)
        log_texts = []

        for i in range(current_turn + 1):
            if not self.logs[i]:
                continue
            if "log" not in self.logs[i]:
                log_entry = f"Turn {self.logs[i]['turn']}: undefined log"
            else:
                log_entry = f"Turn {self.logs[i]['turn']}: {self.logs[i]['log']}"
            log_texts.append(log_entry)

        # Ensure the starting index is within valid range
        self.current_log_index = max(0, min(self.current_log_index, len(log_texts) - self.lines_per_page))

        # Display the logs that fit within the viewable area
        visible_logs = log_texts[self.current_log_index:self.current_log_index + self.lines_per_page]

        for i, log_entry in enumerate(visible_logs):
            log_text = font.render(log_entry, True, (200, 200, 200))
            screen.blit(log_text, (log_area_rect.x + 10, log_area_rect.y + i * 20))

        # Draw a border around the log area
        pygame.draw.rect(screen, (100, 100, 100), log_area_rect, 2)

        # Draw Up and Down buttons for scrolling
        button_margin = 10
        button_x = log_area_rect.right - 35  # Adjusted to fit next to the log area
        button_y_up = log_area_top - 40  # Above the log area
        button_y_down = log_area_top + 300 + button_margin  # Below the log area

        self.scroll_button_up_rect = pygame.Rect(button_x - 25, button_y_up, 30, 30)
        self.scroll_button_down_rect = pygame.Rect(button_x - 25, button_y_down, 30, 30)

        screen.blit(self.button_images["up"], self.scroll_button_up_rect.topleft)
        screen.blit(self.button_images["down"], self.scroll_button_down_rect.topleft)

    def draw_control_buttons(self, screen, sidebar_x, button_area_top):
        button_offset_x = sidebar_x + 10
        button_offset_y = button_area_top

        self.buttons["previous"].topleft = (button_offset_x, button_offset_y)
        self.buttons["play_stop"].topleft = (button_offset_x + 60, button_offset_y)
        self.buttons["next"].topleft = (button_offset_x + 120, button_offset_y)

        screen.blit(self.button_images["previous"], self.buttons["previous"].topleft)
        play_stop_image = (
            self.button_images["pause"]
            if self.buttons["playing"]
            else self.button_images["play"]
        )
        screen.blit(play_stop_image, self.buttons["play_stop"].topleft)
        screen.blit(self.button_images["next"], self.buttons["next"].topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Scroll Up
            if self.scroll_button_up_rect.collidepoint(event.pos):
                self.current_log_index = max(0, self.current_log_index - 1)
            # Scroll Down
            elif self.scroll_button_down_rect.collidepoint(event.pos):
                max_index = max(0, len(self.logs) - self.lines_per_page)
                self.current_log_index = min(self.current_log_index + 1, max_index)
            else:
                if self.buttons["previous"].collidepoint(event.pos):
                    if self.on_previous:  # Call the callback if set
                        self.on_previous()
                elif self.buttons["next"].collidepoint(event.pos):
                    if self.on_next:  # Call the callback if set
                        self.on_next()
                elif self.buttons["play_stop"].collidepoint(event.pos):
                    if self.on_play_stop:  # Call the callback if set
                        self.on_play_stop()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Check if Escape key is pressed
                return "menu"
        return True
