import pygame
import Entity
import Inventory

class Player(Entity.Entity):# pygame.sprite.Sprite):
    def __init__(self, texture):
        super().__init__(   texture,    (100,100),  (400,400),  100,    5)
        #                   ^ img file  ^ size      ^start pos  ^health ^speed
        self.points = 0 #probably best to store points/money directly, rather than in inventory
        self.inventory = Inventory.Inventory()
    
    #def move(self):
    #    super().move()