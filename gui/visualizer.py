import pygame
import json
from gui import *
from gui.config import *
from gui.grid import Grid
from gui.sidebar import Sidebar
from gui.menu import Menu
from gui.level_page import LevelPage
from gui.player import Player
import gui.config as config
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="PIL")

class Visualizer:
    def __init__(self, FILENAME):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Wumpus World")
        self.state = self.load_state(FILENAME)
        self.current_turn_index = 0
        self.playing = False
        self.frame_count = 0
        self.clock = pygame.time.Clock()
        self.update_grid_size()
        self.buttons = {
            "previous": pygame.Rect(50, 50, 50, 50),
            "next": pygame.Rect(110, 50, 50, 50),
            "play_stop": pygame.Rect(170, 50, 50, 50),
            "playing": False,
        }

        # Initialize Menu
        self.menu = Menu()
        self.menu_active = True

        # Initialize Grid, Player, and Sidebar
        self.grid = Grid(self.get_current_map(), offset=self.offset)
        self.player = Player(offset=self.offset)

        # Pass callbacks to Sidebar for state management
        self.sidebar = Sidebar(
            self.buttons, 
            self.state, 
            offset=self.offset,
            on_previous=self.previous_turn,
            on_next=self.next_turn,
            on_play_stop=self.toggle_playing
        )

    def update_grid_size(self):
        current_map = self.get_current_map()
        self.map_rows = len(current_map)
        self.map_cols = len(current_map[0])

        # Calculate new grid size
        new_grid_size = min(
            WINDOW_HEIGHT // self.map_rows, WINDOW_WIDTH // self.map_cols
        )

        # Calculate new offset
        self.offset = (
            (WINDOW_WIDTH - new_grid_size * self.map_cols) / 2,
            (WINDOW_HEIGHT - new_grid_size * self.map_rows) / 2,
        )

        # Calculate ratio for resizing
        ratio = new_grid_size / config.GRID_SIZE

        # Update global grid size
        config.GRID_SIZE = new_grid_size

        # Update player image size proportionally
        config.PLAYER_IMAGE_SIZE = (
            int(config.PLAYER_IMAGE_SIZE[0] * ratio),
            int(config.PLAYER_IMAGE_SIZE[1] * ratio),
        )

    def load_state(self, filename):
        with open(filename, "r") as f:
            return json.load(f)

    def get_current_turn(self):
        return self.current_turn_index
    
    def get_current_state(self):
        return self.state[self.current_turn_index]

    def get_current_map(self):
        return self.state[self.current_turn_index]["map"]

    def previous_turn(self):
        self.current_turn_index = max(0, self.current_turn_index - 1)
        self.update_grid_size()

    def next_turn(self):
        self.current_turn_index = min(len(self.state) - 1, self.current_turn_index + 1)
        self.update_grid_size()

    def toggle_playing(self):
        self.playing = not self.playing
        self.buttons["playing"] = self.playing

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.sidebar.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if Escape key is pressed
                    return "menu"
        return True

    def update_state(self):
        if self.playing and self.frame_count % STATE_DELAY == 0:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.state)
            if self.current_turn_index == len(self.state) - 1:
                self.playing = False
            self.update_grid_size()  # Update grid size when changing state

    def draw(self):
        self.grid.update_grid(self.get_current_map())
        self.grid.draw(self.screen)
        self.player.draw(self.screen, self.get_current_state(), self.frame_count)
        self.sidebar.draw(self.screen, self.get_current_turn())
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            result = self.handle_events()
            if result == "menu":
                return "menu"
            elif not result:
                running = False
            else:
                self.update_state()
                self.draw()
            self.frame_count += 1
            self.clock.tick(60)
        pygame.quit()

def visualize():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Wumpus World")

    # Initialize Menu and other pages
    menu = Menu()
    current_page = menu
    level_page = None
    visualizer = None

    # Main game loop
    running = True
    while running:
        if isinstance(current_page, Menu):
            result = current_page.handle_events()
            if result == "exit":
                running = False
            elif result in ["lv1"]:
                level_page = LevelPage(result)
                current_page = level_page

        elif isinstance(current_page, LevelPage):
            result = current_page.handle_events()
            if result == "exit":
                running = False
            elif result == "menu":
                current_page = menu
            elif result:
                visualizer = Visualizer(f"Assets/JSON/{result}")
                current_page = visualizer

        elif isinstance(current_page, Visualizer):
            result = current_page.run()
            if result == "menu":
                current_page = menu

        if isinstance(current_page, Menu) or isinstance(current_page, LevelPage):
            # current page it's level page handle hover events
            if isinstance(current_page, LevelPage):
                current_page.handle_mouse_motion()
            current_page.draw(screen)

    pygame.quit()
