import pygame
import os
from gui.config import *

class Sidebar:
    def __init__(self, buttons, logs, offset=(0, 0), on_previous=None, on_next=None, on_play_stop=None):
        self.buttons = buttons
        self.logs = logs
        self.offset = offset
        self.load_button_images()
        self.current_log_index = 0
        self.lines_per_page = 15
        self.on_previous = on_previous
        self.on_next = on_next
        self.on_play_stop = on_play_stop
        self.reached_end = False

    def load_button_images(self):
        self.button_images = {
            "previous": pygame.image.load(
                os.path.join(CONTROLBUTTON_FOLDER, "prev.png")
            ),
            "next": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "next.png")),
            "play": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "play.png")),
            "pause": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "pause.png")),
            "up": pygame.image.load((CONTROLBUTTON_FOLDER + "/up.png")),
            "down": pygame.image.load((CONTROLBUTTON_FOLDER + "/down.png")),
            "previous_hover": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "prev_hover.png")),
            "next_hover": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "next_hover.png")),
            "play_hover": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "play_hover.png")),
            "pause_hover": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "pause_hover.png")),
            "up_hover": pygame.image.load((CONTROLBUTTON_FOLDER + "/up_hover.png")),
            "down_hover": pygame.image.load((CONTROLBUTTON_FOLDER + "/down_hover.png")),
        }
        
        for key in self.button_images:
            self.button_images[key] = pygame.transform.scale(
                self.button_images[key], (30, 30)
            )

    def draw(self, screen, current_turn, move_log=False):
        sidebar_bg_color = (50, 50, 50)
        sidebar_x = WINDOW_SIZE[0] - SIDEBAR_WIDTH + self.offset[0]
        sidebar_y = self.offset[1]
        sidebar_width = SIDEBAR_WIDTH
        sidebar_height = WINDOW_SIZE[1]

        if move_log:
            self.current_log_index = current_turn - 14

        pygame.draw.rect(
            screen,
            sidebar_bg_color,
            (sidebar_x, sidebar_y, sidebar_width, sidebar_height),
        )

        pygame.draw.rect(
            screen, (30, 30, 30), (sidebar_x, sidebar_y, sidebar_width, sidebar_height), 2
        )

        latest_log = self.logs[current_turn]
        self.draw_player_properties(screen, sidebar_x, sidebar_y, latest_log)

        log_area_top = sidebar_y + 280
        self.draw_scrollable_log(screen, sidebar_x, log_area_top, sidebar_width, current_turn)

        button_area_top = sidebar_height - 80
        self.draw_control_buttons(screen, sidebar_x, button_area_top)

    def draw_player_properties(self, screen, sidebar_x, sidebar_y, data):
        font = pygame.font.Font(None, 24)
        title_font = pygame.font.Font(None, 30)

        title_text = title_font.render("Player Stats", True, (255, 255, 255))
        screen.blit(title_text, (sidebar_x + 10, sidebar_y + 10))

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
        log_area_rect = pygame.Rect(sidebar_x + 10, log_area_top, sidebar_width - 20, 320)
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

        self.current_log_index = max(0, min(self.current_log_index, len(log_texts) - self.lines_per_page))
        visible_logs = log_texts[self.current_log_index:self.current_log_index + self.lines_per_page]

        for i, log_entry in enumerate(visible_logs):
            log_text = font.render(log_entry, True, (200, 200, 200))
            if "Heal" in log_entry:
                log_text = font.render(log_entry, True, (0, 255, 0))
            if "Over" in log_entry:
                log_text = font.render(log_entry, True, (255, 0, 0))
            if "Grab Gold" in log_entry:
                log_text = font.render(log_entry, True, (255, 255, 0))
            screen.blit(log_text, (log_area_rect.x + 10, log_area_rect.y + i * 20 + 10))

        pygame.draw.rect(screen, (100, 100, 100), log_area_rect, 2)

        button_margin = 10
        button_x = log_area_rect.right - 35
        button_y_up = log_area_top - 40
        button_y_down = log_area_top + 320 + button_margin

        self.scroll_button_up_rect = pygame.Rect(button_x - 25, button_y_up, 30, 30)
        self.scroll_button_down_rect = pygame.Rect(button_x - 25, button_y_down, 30, 30)

        mouse_pos = pygame.mouse.get_pos()

        # Draw Up button with hover effect
        if self.scroll_button_up_rect.collidepoint(mouse_pos):
            screen.blit(self.button_images["up_hover"], self.scroll_button_up_rect.topleft)
        else:
            screen.blit(self.button_images["up"], self.scroll_button_up_rect.topleft)

        # Draw Down button with hover effect
        if self.scroll_button_down_rect.collidepoint(mouse_pos):
            screen.blit(self.button_images["down_hover"], self.scroll_button_down_rect.topleft)
        else:
            screen.blit(self.button_images["down"], self.scroll_button_down_rect.topleft)

    def draw_control_buttons(self, screen, sidebar_x, button_area_top):
        button_offset_x = sidebar_x + 10
        button_offset_y = button_area_top

        self.buttons["previous"].topleft = (button_offset_x, button_offset_y)
        self.buttons["play_stop"].topleft = (button_offset_x + 60, button_offset_y)
        self.buttons["next"].topleft = (button_offset_x + 120, button_offset_y)

        mouse_pos = pygame.mouse.get_pos()

        if self.buttons["previous"].collidepoint(mouse_pos):
            screen.blit(self.button_images["previous_hover"], self.buttons["previous"].topleft)
        else:
            screen.blit(self.button_images["previous"], self.buttons["previous"].topleft)

        if self.buttons["play_stop"].collidepoint(mouse_pos):
            play_stop_image = (
                self.button_images["pause_hover"]
                if self.buttons["playing"]
                else self.button_images["play_hover"]
            )
        else:
            play_stop_image = (
                self.button_images["pause"]
                if self.buttons["playing"]
                else self.button_images["play"]
            )
        screen.blit(play_stop_image, self.buttons["play_stop"].topleft)

        if self.buttons["next"].collidepoint(mouse_pos):
            screen.blit(self.button_images["next_hover"], self.buttons["next"].topleft)
        else:
            screen.blit(self.button_images["next"], self.buttons["next"].topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.scroll_button_up_rect.collidepoint(event.pos):
                self.current_log_index = max(0, self.current_log_index - 1)
            elif self.scroll_button_down_rect.collidepoint(event.pos):
                max_index = max(0, len(self.logs) - self.lines_per_page)
                self.current_log_index = min(self.current_log_index + 1, max_index)
            else:
                if self.buttons["previous"].collidepoint(event.pos):
                    if self.on_previous:
                        self.on_previous()
                elif self.buttons["next"].collidepoint(event.pos):
                    if self.on_next:
                        self.on_next()
                elif self.buttons["play_stop"].collidepoint(event.pos):
                    if self.on_play_stop:
                        self.on_play_stop()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
        return True
