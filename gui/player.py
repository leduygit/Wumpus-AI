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
        self.number_of_moving_frames = 8
        self.attack_frames = 9
        self.load_images()
        self.offset = offset

    def load_images(self):
        self.player_images["Player"] = {
            "left": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/left-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(8)
            ],
            "right": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/right-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(8)
            ],
            "up": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/back-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(8)
            ],
            "down": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/front-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(8)
            ],
            "attack_down": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/attack-front-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(self.attack_frames)
            ],
            "attack_up": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/attack-back-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(self.attack_frames)
            ],
            "attack_left": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/attack-left-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(self.attack_frames)
            ],
            "attack_right": [
                pygame.transform.scale(
                    pygame.image.load(f"{config.PLAYER_FOLDER_PATH}/attack-right-{i}.png"),
                    config.PLAYER_IMAGE_SIZE,
                )
                for i in range(self.attack_frames)
            ]
        }

    def get_player_image(self, player_name, direction, frame, is_atacking=False):
        if is_atacking:
            return self.player_images[player_name][f"attack_{(direction)}"][frame % self.attack_frames]
        return self.player_images[player_name][direction][frame % self.number_of_moving_frames]

    def draw(self, screen, current_state, frame_count, is_atacking):
        current_position = current_state["position"]
        direction = direction_map[current_state["direction"]]
        player_image = self.get_player_image(
            "Player", direction, frame_count // config.FRAME_DELAY, is_atacking
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