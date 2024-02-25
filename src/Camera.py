import pygame
from Renderable import Renderable

class Camera:
    def __init__(self, target:Renderable, width, height):
        self.target = target
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)

    def apply(self, target_rect):
        return target_rect.move(self.rect.topleft)

    def update(self):
        x = 0
        y = max(-self.target.rect.centery + self.height // 2, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)