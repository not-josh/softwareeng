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
        dx = player_pos[0] - self.get_rect().centerx
        dy = player_pos[1] - self.get_rect().centery
        distance = math.sqrt(dx * dx + dy * dy)
        move = (dx/distance * self.speed, dy/distance * self.speed)
        checked_mvoe = super().move(move)
        self.normalizeMove(checked_mvoe)