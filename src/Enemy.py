import Entity
import math
import pygame
import Player
import SETTINGS

class Enemy(Entity.GroundEntity):
    def __init__(self, folder:str, map, size, pos, health:int, speed:int, attack_damage:int):
        super().__init__(folder, map, size, pos, health, speed)
        self.folder = folder
        self.attack_damage:int = attack_damage
        self.attack_cooldown_max:int = SETTINGS.ENEMY_MELEE_COOLDOWN
        self.attack_cooldown:int = 0

    def melee_attack(self, player:Player.Player):
        self.attack_cooldown = max(self.attack_cooldown-1, 0)
        if (self.attack_cooldown == 0):
            if (self.get_rect().colliderect(player.get_rect())):
                player.lower_health(self.attack_damage)
                self.attack_cooldown = self.attack_cooldown_max


    def update(self, player:Player.Player):
        if (self.alive):
            self.move(player.get_rect().center)

    def move(self, player_pos:tuple[int,int]):  #CENTER of player rect
        move = [0,0]
        horizontal_direction = 0    #   These keep track of horizontal and vertical direction. Left and down are -1,
        vertical_direction = 0      #   right and up are +1. These are used for changing direction image and for normalizing movement
        if (player_pos[0] < self.rect.center[0]):
            move[0] -= self.speed
            horizontal_direction -= 1
        if (player_pos[0] > self.rect.center[0]):
            move[0] += self.speed
            horizontal_direction += 1
        if (player_pos[1] < self.rect.center[1]):
            move[1] -= self.speed
            vertical_direction -= 1
        if (player_pos[1] > self.rect.center[1]):
            move[1] += self.speed
            vertical_direction += 1

        if (move[0] != 0) and (move[1] != 0):
            adjusted_speed = math.sqrt((self.speed*self.speed)/2)
            move[0] = adjusted_speed * horizontal_direction
            move[1] = adjusted_speed * vertical_direction
        
        if (horizontal_direction == -1):
            self.rect.centerx = max(player_pos[0], self.rect.centerx + move[0])
        elif (horizontal_direction == 1):
            self.rect.centerx = min(player_pos[0], self.rect.centerx + move[0])

        if (vertical_direction == -1):
            self.rect.centery = max(player_pos[1], self.rect.centery + move[1])
        elif (vertical_direction == 1):
            self.rect.centery = min(player_pos[1], self.rect.centery + move[1])