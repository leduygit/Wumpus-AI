import pygame
from gui.config import WINDOW_SIZE


class Menu:
    def __init__(self):
        # Define button names
        self.button_names = ["lv1", "exit"]

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
        button_y = WINDOW_SIZE[1] // 2 - 100
        self.button_rects = [
            img.get_rect(center=(WINDOW_SIZE[0] // 2, button_y + i * 100))
            for i, img in enumerate(self.button_images)
        ]

        self.hovered_button = None  # Track which button is hovered

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw buttons with hover effect
        for i, rect in enumerate(self.button_rects):
            if self.hovered_button == self.button_names[i]:
                screen.blit(self.button_hover_images[i], rect.topleft)
            else:
                screen.blit(self.button_images[i], rect.topleft)

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
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.hovered_button = self.button_names[i]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        return self.button_names[i]

        return None
