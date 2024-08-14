import pygame
from gui.config import WINDOW_SIZE


class Menu:
    def __init__(self):
        # Define button names
        self.button_names = ["start", "exit"]

        # Load images
        self.background = pygame.image.load("assets/images/menu/background.png")
        self.button_images = [
            pygame.image.load(f"assets/images/menu/{name}.png")
            for name in self.button_names
        ]
        self.button_hover_images = [
            pygame.image.load(f"assets/images/menu/{name}-2.png")
            for name in self.button_names
        ]

        # Scale the menu background to fit the window size
        self.background = pygame.transform.scale(self.background, WINDOW_SIZE)

        # Create button rectangles
        # button_y = WINDOW_SIZE[1] // 2 
        # self.button_rects = [
        #     img.get_rect(center=(WINDOW_SIZE[0] // 2, button_y + i * 100))
        #     for i, img in enumerate(self.button_images)
        # ]
        self.start_button = {
            "image": self.button_images[0],
            "hover_image": self.button_hover_images[0],
            "center": (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2),
        }

        self.exit_button = {
            "image": self.button_images[1],
            "hover_image": self.button_hover_images[1],
            "center": (WINDOW_SIZE[0] * 8 / 9, WINDOW_SIZE[1] * 10 / 11),
        }

        self.hovered_button = None  # Track which button is hovered

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw buttons with hover effect
        start_button_image = self.start_button["hover_image"] if self.hovered_button == "start" else self.start_button["image"]
        exit_button_image = self.exit_button["hover_image"] if self.hovered_button == "exit" else self.exit_button["image"]
        screen.blit(start_button_image, self.start_button["image"].get_rect(center=self.start_button["center"]).topleft)
        screen.blit(exit_button_image, self.exit_button["image"].get_rect(center=self.exit_button["center"]).topleft)

        pygame.display.flip()

    def handle_events(self):
        mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

        # Update hovered button based on mouse position
        if mouse_pos:
            self.hovered_button = None
            if self.start_button["image"].get_rect(center=self.start_button["center"]).collidepoint(mouse_pos):
                self.hovered_button = "start"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return "start"
            elif self.exit_button["image"].get_rect(center=self.exit_button["center"]).collidepoint(mouse_pos):
                self.hovered_button = "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return "exit"

        return None
