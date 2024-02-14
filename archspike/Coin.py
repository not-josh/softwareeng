import pygame

class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        # affects height and width
        self.image = pygame.image.load("Assets/1_coin.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)