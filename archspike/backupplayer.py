import pygame

red = (255, 0, 0)


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        # affects height and width
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.coin_count = 0

    # Updating based on inputs
    def update(self, coords):
        self.rect.x += coords[0]
        self.rect.y += coords[1]
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_LEFT]:
        #    self.rect.x -= self.speed
        #if keys[pygame.K_RIGHT]:
        #    self.rect.x += self.speed
        #if keys[pygame.K_UP]:
        #    self.rect.y -= self.speed
        #if keys[pygame.K_DOWN]:
        #    self.rect.y += self.speed

    # Gets future position if the player is allowed to move
    def get_pos_change(self):
        pos_change = [0,0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pos_change[0] -= self.speed
        if keys[pygame.K_RIGHT]:
            pos_change[0] += self.speed
        if keys[pygame.K_UP]:
            pos_change[1] -= self.speed
        if keys[pygame.K_DOWN]:
            pos_change[1] += self.speed
        return pos_change