import pygame
import Renderable

class Entity(Renderable.Renderable):
    def __init__(self, texture, size, pos, health, speed):
        super().__init__(   texture + "/idle.png",      (100,100),  (400,400))
        #                   ^ img file                  ^ size      ^start pos
        self.texture_folder = texture
        self.speed = speed
        self.health = health
        self.direction = 'r'

    def move(self):
        move = [0,0]
        dir = "none"
        if (pygame.key.get_pressed()[pygame.K_a]):
            move[0] -= self.speed
            dir = "left.png"
            #self.surface = pygame.image.load(self.texture_folder + "left.png")
        if (pygame.key.get_pressed()[pygame.K_d]):
            move[0] += self.speed
            dir = "right.png"
            #new_direction = 'r'
            #self.surface = pygame.image.load(self.texture_folder + "right.png")
        if (pygame.key.get_pressed()[pygame.K_w]):
            move[1] -= self.speed
            dir = "up.png"
            #self.surface = pygame.image.load(self.texture_folder + "up.png")
        if (pygame.key.get_pressed()[pygame.K_s]):
            move[1] += self.speed
            dir = "down.png"
            #self.surface = pygame.image.load(self.texture_folder + "down.png")
        if (dir != "none"):
            self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + dir),self.size)
        self.rect.left += move[0]
        self.rect.top += move[1]