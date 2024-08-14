import pygame
from gui.config import *
import gui.config as config
from gui.utils import *
from gui.animation_object import AnimationObject

class Grid:
    def __init__(self, grid_data, offset=(0, 0)):
        self.grid_data = grid_data
        self.offset = offset
        self.dynamic_font = pygame.font.SysFont(
            "Roboto", max(12, config.GRID_SIZE // 2)
        )
        self.road_image = load_images(config.ROAD_FOLDER_PATH + "/road.png")
        self.player_image = load_folder_images(config.PLAYER_FOLDER_PATH)[0]
        self.wumpus_image = load_folder_images(config.ENEMY_FOLDER_PATH)[0]
        self.pit_image = load_images(config.OBSTACLE_FOLDER_PATH + "/pit.png")
        self.poison_gas_animation = AnimationObject(config.OBSTACLE_FOLDER_PATH + "/PoisonGas", offset)
        self.gold_image = load_images(config.OBSTACLE_FOLDER_PATH + "/gold.png", ratio=1)
        self.healing_potion_animation = AnimationObject(config.OBSTACLE_FOLDER_PATH + "/HealingPotion", offset)
        self.door_image = load_images(config.ROAD_FOLDER_PATH + "/door.png")

        self.breeze_image = load_images(config.EFFECT_FOLDER_PATH + "/breeze.png", ratio = config.PERCEPT_RATIO)
        self.whiff_image = load_images(config.EFFECT_FOLDER_PATH + "/whiff.png", ratio = config.PERCEPT_RATIO)
        self.glow_image = load_images(config.EFFECT_FOLDER_PATH + "/glow.png", ratio = config.PERCEPT_RATIO)
        self.stench_image = load_images(config.EFFECT_FOLDER_PATH + "/stench.png", ratio = config.PERCEPT_RATIO)

    def update_grid(self, grid_data):
        self.grid_data = grid_data

    def draw(self, screen, frame):
        self.frame = frame
        screen.fill(WHITE)
        self._draw_grid(screen)

    def _draw_grid(self, screen):
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                self._draw_cell(screen, row, col)

    def _draw_image(self, screen, image, position):
        # get image size
        image_size = image.get_size()
        position = (position[0] * config.GRID_SIZE + self.offset[0] + (config.GRID_SIZE - image_size[0]) / 2, position[1] * config.GRID_SIZE + (config.GRID_SIZE - image_size[1]) / 2 + self.offset[1])
        screen.blit(image, position)

    def _draw_cell(self, screen, row, col):

        self._draw_cell_border(screen, row, col)
        
        self._draw_image(screen, self.road_image, (col, row))
        
        if "P" in self.grid_data[row][col]:
            self._draw_image(screen, self.pit_image, (col, row))
        if "P_G" in self.grid_data[row][col]:
            # self._draw_image(screen, self.gas_image, (col, row))
            self.poison_gas_animation.draw(screen, (row, col), self.frame)
        if "D" in self.grid_data[row][col]:
            self._draw_image(screen, self.door_image, (col, row))
        if "W" in self.grid_data[row][col]:
            self._draw_image(screen, self.wumpus_image, (col, row))
        if "H_P" in self.grid_data[row][col]:
            # self._draw_image(screen, self.healing_potion_image, (col, row))
            self.healing_potion_animation.draw(screen, (row, col), self.frame)
        if "G" in self.grid_data[row][col]:
            self._draw_image(screen, self.gold_image, (col, row))

        cell_value = ""

        if "S" in self.grid_data[row][col]:
            position = (col * config.GRID_SIZE + self.offset[0], row * config.GRID_SIZE + self.offset[1])
            screen.blit(self.stench_image, position)
        if "B" in self.grid_data[row][col]:
            position = (col * config.GRID_SIZE + self.offset[0] + config.GRID_SIZE * (1 - config.PERCEPT_RATIO), row * config.GRID_SIZE + self.offset[1])
            screen.blit(self.breeze_image, position)
        if "G_L" in self.grid_data[row][col]:
            position = (col * config.GRID_SIZE + self.offset[0], row * config.GRID_SIZE + self.offset[1] + config.GRID_SIZE * (1 - config.PERCEPT_RATIO))
            screen.blit(self.glow_image, position)
        if "W_H" in self.grid_data[row][col]:
            position = (col * config.GRID_SIZE + self.offset[0]  + config.GRID_SIZE * (1 - config.PERCEPT_RATIO), row * config.GRID_SIZE + self.offset[1] + config.GRID_SIZE * (1 - config.PERCEPT_RATIO))
            screen.blit(self.whiff_image, position)

        if "?" in self.grid_data[row][col]:
            self._apply_blur_to_cell(screen, row, col)

    def _draw_cell_border(self, screen, row, col):
        border_color = LITE_BLACK
        pygame.draw.rect(
            screen,
            border_color,
            (
                col * config.GRID_SIZE + self.offset[0],
                row * config.GRID_SIZE + self.offset[1],
                config.GRID_SIZE,
                config.GRID_SIZE,
            ),
            1,
        )

    def _apply_blur_to_cell(self, screen, row, col):
        cell_rect = pygame.Rect(
            col * config.GRID_SIZE + self.offset[0],
            row * config.GRID_SIZE + self.offset[1],
            config.GRID_SIZE,
            config.GRID_SIZE,
        )

        # Instead of blurring, just darken the cell directly
        dark_surface = pygame.Surface((config.GRID_SIZE, config.GRID_SIZE))
        dark_surface.fill((0, 0, 0))
        dark_surface.set_alpha(176)  # Adjust alpha to control darkness level (0-255)

        # Blit the darkening surface directly onto the screen
        screen.blit(dark_surface, cell_rect.topleft)



    def _blur_surface(self, surface):
        blur_radius = 1  # Adjust this for stronger or weaker blur
        array = pygame.surfarray.pixels3d(surface)

        for _ in range(blur_radius):
            array[:-1, :-1] = (array[:-1, :-1] + array[1:, :-1] + array[:-1, 1:] + array[1:, 1:]) // 4
            array[1:, :-1] = (array[1:, :-1] + array[:-1, :-1] + array[1:, 1:] + array[:-1, 1:]) // 4
            array[:-1, 1:] = (array[:-1, 1:] + array[:-1, :-1] + array[1:, 1:] + array[1:, :-1]) // 4
            array[1:, 1:] = (array[1:, 1:] + array[1:, :-1] + array[:-1, 1:] + array[:-1, :-1]) // 4

        return pygame.surfarray.make_surface(array)


    def _draw_text(self, screen, text_value, row, col, offset=(0, 0)):
        text_value = str(text_value)
        text_color = BLACK
        text_surface = self.dynamic_font.render(text_value, True, text_color)
        text_rect = text_surface.get_rect(
            center=(
                col * config.GRID_SIZE
                + config.GRID_SIZE // 2
                + self.offset[0]
                + offset[0],
                row * config.GRID_SIZE
                + config.GRID_SIZE // 2
                + self.offset[1]
                + offset[1],
            )
        )
        screen.blit(text_surface, text_rect)