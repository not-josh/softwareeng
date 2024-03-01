import pygame
import Renderable

class Entity(Renderable.Renderable):
    def __init__(self, texture, size, pos, health, speed):
        super().__init__(   texture,      size,  pos)
        #                   ^ img file                  ^ size      ^start pos
        #self.texture_folder = folder
        self.speed = speed
        self.health:int = health
        self.max_health = health
        self.alive = True
        self.floatx:float = pos[0]
        self.floaty:float = pos[1]

    def lower_health(self, value:int):
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
            self.lower_health(self.health-self.max_health)

    def increase_max_health(self, increase:int):
        old_max_health = self.max_health
        self.max_health += increase
        if (old_max_health != 0):
            self.health = int(self.health * (self.max_health / old_max_health))
    def kill(self):
        self.health = 0
        self.alive = False
        