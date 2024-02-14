import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, texture):
        self.speed = 5
        self.surface = pygame.transform.scale(pygame.image.load(texture),(100,100))
        self.rect = pygame.Rect(100,100,10,10)
    
    def move(self):
        move = [0,0]
        if (pygame.key.get_pressed()[pygame.K_a]):
            move[0] -= self.speed
        if (pygame.key.get_pressed()[pygame.K_d]):
            move[0] += self.speed
        if (pygame.key.get_pressed()[pygame.K_w]):
            move[1] -= self.speed
        if (pygame.key.get_pressed()[pygame.K_s]):
            move[1] += self.speed
        self.rect.left += move[0]
        self.rect.top += move[1]