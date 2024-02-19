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
