from gui.utils import *

class AnimationObject():
    def __init__(self, image_folder, offset=(0, 0)):
        self.images = load_folder_images(image_folder)
        self.total_frame = len(self.images)
        self.offset = offset
        self.slow_factor = 2

    def draw(self, screen, position, frame):
        row, col = position
        position = (col * config.GRID_SIZE + self.offset[0], row * config.GRID_SIZE + self.offset[1])
        current_frame = int((frame // self.slow_factor) / self.total_frame)
        screen.blit(self.images[current_frame % self.total_frame], position)