import pygame
import Renderable

class Entity(Renderable.Renderable):
    def __init__(self, texture, size, pos, health, speed):
        super().__init__(   texture + "/idle.png",      (100,100),  (400,400))
        #                   ^ img file                  ^ size      ^start pos
        self.texture_folder = texture
        self.speed = speed
        self.health, self.max_health = health
        self.direction = 'r'
        self.alive = True

    def damage(self, value:int):
        self.health -= value
        self.health = max(0,self.health)
        if (self.health == 0):
            self.alive = False

    def increase_health(self, value:int):
        self.health += value
        self.health = min(self.health, self.max_health)

    def lower_max_health(self, decrease:int):
        self.max_health -= decrease
        self.max_health = max(0, self.max_health)
        if (self.max_health < self.health):
            self.damage(self.health-self.max_health)

    def increase_max_health(self, increase:int):
        self.max_health += increase