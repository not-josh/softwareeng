import pygame

class Entity:
    def __init__(self, texture, size, pos, health, speed):
        self.surface = pygame.transform.scale(pygame.image.load(texture),size)
        self.rect = self.surface.get_rect()
        self.rect.topleft = pos

        self.speed = speed
        self.health = health

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