import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LITE_BLACK = (0, 0, 0, 30)
GRAY = (200, 200, 200)

# Folders
CONTROLBUTTON_FOLDER = "assets/images/ControlButtons"
ROAD_FOLDER_PATH = "assets/images/Road"
PLAYER_FOLDER_PATH = "assets/images/Agent/Player"
ENEMY_FOLDER_PATH = "assets/images/Agent/Wumpus"
OBSTACLE_FOLDER_PATH = "assets/images/Obstacle" # pit, Gas, Gold, healing_potion
EFFECT_FOLDER_PATH = "assets/images/Effect" # Breeze, Whiff, Glow, Stench
ARROW_FOLDER_PATH = "assets/images/Arrow"

# window size : 1280 x 800
# Constants
MAX_WIDTH = 10
MAX_HEIGHT = 10
GRID_SIZE = 32
WINDOW_WIDTH = 880
WINDOW_HEIGHT = 800
SIDEBAR_WIDTH = 400
WINDOW_SIZE = (WINDOW_WIDTH + SIDEBAR_WIDTH, WINDOW_HEIGHT)
BUTTON_HEIGHT = 40
PLAYER_IMAGE_SIZE = (22.5, 30)
FRAME_DELAY = 5
STATE_DELAY = 60

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont("Roboto", 19)
