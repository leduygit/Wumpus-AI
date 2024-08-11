import pygame
import gui.config as config

class Arrow:
    def __init__(self, direction, grid_size, offset):
        self.direction = direction
        self.grid_size = grid_size
        self.offset = offset
        self.arrow_image = self.load_arrow_image()
        self.arrow_scale_ratio = 2

    def load_arrow_image(self, direction = "R"):
        arrow_image = pygame.image.load(config.ARROW_FOLDER_PATH + "/arrow_right.png")
        if self.direction == "L":
            arrow_image = pygame.transform.rotate(arrow_image, 180)
        elif self.direction == "U":
            arrow_image = pygame.transform.rotate(arrow_image, 90)
        elif self.direction == "D":
            arrow_image = pygame.transform.rotate(arrow_image, -90)
        return pygame.transform.scale(arrow_image, (self.grid_size // 2, self.grid_size // 2)) # Scale down by 2

    def draw(self, screen, current_frame, position):
        if self.direction == "L":
            delta = (- current_frame * self.grid_size / config.STATE_DELAY, 0) # 30 is STATE_DELAY
        elif self.direction == "U":
            delta = (0, -current_frame * self.grid_size / config.STATE_DELAY)
        elif self.direction == "D":
            delta = (0, current_frame * self.grid_size / config.STATE_DELAY)
        else:
            delta = (current_frame * self.grid_size / config.STATE_DELAY, 0)
        position = (position[0] + delta[0] + self.grid_size / 4, position[1] + delta[1] + self.grid_size / 4)
        # Note: The arrow is drawn at the center of the cell as the position is the top-left corner (the image had been scaled down by 2)
        screen.blit(self.arrow_image, position)
