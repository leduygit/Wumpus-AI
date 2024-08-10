# player.py
import pygame
import gui.config as config

direction_map = {
    "R" : "right",
    "L" : "left",
    "U" : "up",
    "D" : "down"
}

class Player:
    def __init__(self, offset=(0, 0)):
        self.player_images = {}
        self.previous_positions = {}
        self.previous_move = {}
        self.load_images()
        self.offset = offset
        self.number_of_frames = 1

    def load_images(self):
        self.player_images["Player"] = {
            "left": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/agent_left.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(1)
            ],
            "right": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/agent_right.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(1)
            ],
            "up": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/agent_up.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(1)
            ],
            "down": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/agent_down.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(1)
            ],
        }

    def get_player_image(self, player_name, direction, frame):
        return self.player_images[player_name][direction][frame % self.number_of_frames]

    def draw(self, screen, current_state, frame_count):
        current_position = current_state["position"]
        direction = direction_map[current_state["direction"]]
        player_image = self.get_player_image(
            "Player", direction, frame_count // config.FRAME_DELAY
        )
        screen.blit(
            player_image,
            (
                int(current_position[1]) * config.GRID_SIZE
                + self.offset[0]
                + config.GRID_SIZE * 0.15,
                int(current_position[0]) * config.GRID_SIZE + self.offset[1] - 1,
            ),
        )