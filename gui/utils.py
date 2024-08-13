import pygame
import gui.config as config
import os

def load_images(path, ratio = 1):
    try:
        image = load_folder_images(path)
        image = pygame.transform.scale(image[0], (config.GRID_SIZE * ratio, config.GRID_SIZE * ratio))
    except:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (config.GRID_SIZE * ratio, config.GRID_SIZE * ratio))
    return image

def load_folder_images(folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                filename = os.path.join(folder, filename)
                img = pygame.image.load(filename)
                img = pygame.transform.scale(img, (config.GRID_SIZE, config.GRID_SIZE))
                images.append(img)
        return images