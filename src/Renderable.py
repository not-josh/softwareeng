import pygame

class Renderable(pygame.sprite.Sprite):
    def __init__(self, texture, size, pos):
        self.surface = pygame.transform.scale(pygame.image.load(texture),size)
        self.rect = self.surface.get_rect()
        self.rect.topleft = pos
        self.mask = pygame.mask.from_surface(self.surface)