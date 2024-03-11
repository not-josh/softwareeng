import pygame
import math
import Entity
import Collision
import Player

class Projectile(Entity.Entity):
    def __init__(self, texture, size, pos, health, speed, damage:int):
        self.damage = damage
        super().__init__(texture, size, pos, health, speed)

    def update(self, player:Player.Player):
        if player.rect.colliderect(self.rect):
            player.lower_health(self.damage)
            if (self.piercing == False):
                self.kill()