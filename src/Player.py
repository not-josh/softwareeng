import pygame
import Entity
import Inventory
import math

class Player(Entity.Entity):# pygame.sprite.Sprite):
    def __init__(self, texture:str):
        super().__init__(   texture,    (100,100),  (400,400),  100,    5)
        #                   ^ img file  ^ size      ^start pos  ^health ^speed
        self.points = 0 #probably best to store points/money directly, rather than in inventory
        self.inventory = Inventory.Inventory()
    
    def add_points(self, amount:int):
        if (amount < 0):
            raise Exception("Tried to add a negative amount of points")
        else:
            self.points += amount

    def remove_points(self, amount:int):
        if (amount < 0):
            raise Exception("Tried to remove a negative amount of points. Input a positive number of points to be removed.")
        else:
            self.points -= amount
    
    def move(self):
        move = [0,0]
        horizontal_direction = 0
        vertical_direction = 0
        right = 0
        down = 1
        dir = "none"
        if (pygame.key.get_pressed()[pygame.K_a]):
            move[0] -= self.speed
            horizontal_direction -= 1
            #dir = "left.png"
            #self.surface = pygame.image.load(self.texture_folder + "left.png")
        if (pygame.key.get_pressed()[pygame.K_d]):
            move[0] += self.speed
            horizontal_direction += 1
            #dir = "right.png"
            #new_direction = 'r'
            #self.surface = pygame.image.load(self.texture_folder + "right.png")
        if (pygame.key.get_pressed()[pygame.K_w]):
            move[1] -= self.speed
            vertical_direction -= 1
            #dir = "up.png"
            #self.surface = pygame.image.load(self.texture_folder + "up.png")
        if (pygame.key.get_pressed()[pygame.K_s]):
            move[1] += self.speed
            vertical_direction += 1
            #dir = "down.png"
            #self.surface = pygame.image.load(self.texture_folder + "down.png")
        if (dir != "none"):
            self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + dir),self.size)

        if (move[0] != 0) and (move[1] != 0):
            move[0] = math.sqrt((self.speed*self.speed)/2) * horizontal_direction
            move[1] = math.sqrt((self.speed*self.speed)/2) * vertical_direction
        #   ^^ "normalizes" the movement "vector" ^^
        match(horizontal_direction):
            case(-1):
                self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "left.png"),self.size)
            case(1):
                self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "right.png"),self.size)
        match(vertical_direction):
            case(-1):
                self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "up.png"),self.size)
            case(1):
                self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "down.png"),self.size)

        self.rect.left += move[0]
        self.rect.top += move[1]