import pygame

class Camera:
    def __init__(self, target, width, height):
        self.target = target
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)

    def apply(self, target_rect):
        return target_rect.move(self.rect.topleft)

    def update(self):
        x = -self.target.rect.x + self.width // 2
        y = -self.target.rect.y + self.height // 2
        self.rect = pygame.Rect(x, y, self.width, self.height)