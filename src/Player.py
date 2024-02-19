import pygame
import Entity
import Inventory
import math

class Player(Entity.Entity):# pygame.sprite.Sprite):
    def __init__(self, texture):
        super().__init__(   texture,    (100,100),  (400,400),  100,    5)
        #                   ^ img file  ^ size      ^start pos  ^health ^speed
        self.points = 0 #probably best to store points/money directly, rather than in inventory
        self.inventory = Inventory.Inventory()
    
    def move(self):
        move = [0,0]
        right = 1
        down = 1
        dir = "none"
        if (pygame.key.get_pressed()[pygame.K_a]):
            move[0] -= self.speed
            dir = "left.png"
            right = -1
            #self.surface = pygame.image.load(self.texture_folder + "left.png")
        if (pygame.key.get_pressed()[pygame.K_d]):
            move[0] += self.speed
            dir = "right.png"
            right = 1
            #new_direction = 'r'
            #self.surface = pygame.image.load(self.texture_folder + "right.png")
        if (pygame.key.get_pressed()[pygame.K_w]):
            move[1] -= self.speed
            dir = "up.png"
            down = -1
            #self.surface = pygame.image.load(self.texture_folder + "up.png")
        if (pygame.key.get_pressed()[pygame.K_s]):
            move[1] += self.speed
            dir = "down.png"
            down = 1
            #self.surface = pygame.image.load(self.texture_folder + "down.png")
        if (dir != "none"):
            self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + dir),self.size)
        if (move[0] != 0) and (move[1] != 0):
            move[0] = math.sqrt((self.speed*self.speed)/2) * right
            move[1] = math.sqrt((self.speed*self.speed)/2) * down
        self.rect.left += move[0]
        self.rect.top += move[1]