import Entity
import math
import pygame
import Player
import SETTINGS
import StaticMusicManager

class Enemy(Entity.GroundEntity):
    def __init__(self, folder:str, map, size, pos, health:int, attack_damage:int, speed:float = SETTINGS.ENEMY_DEFAULT_SPEED):
        super().__init__(folder, map, size, pos, health, speed)
        self.folder = folder
        self.attack_damage:int = attack_damage
        self.attack_cooldown_max:int = SETTINGS.ENEMY_MELEE_COOLDOWN
        self.attack_cooldown:int = 0
        self.tex_offset = [-3,-6]

    def melee_attack(self, player:Player.Player):
        self.attack_cooldown = max(self.attack_cooldown-1, 0)
        if (self.attack_cooldown == 0):
            if (self.get_rect().colliderect(player.get_rect())) and player.alive:
                player.lower_health(self.attack_damage)
                StaticMusicManager.play_soundfx(SETTINGS.MELEE_ENEMY_ATTACK_SOUND)
                self.attack_cooldown = self.attack_cooldown_max

    def ranged_attack(self, player:Player.Player):
        self.attack_cooldown = max(self.attack_cooldown-1, 0)
        if (self.attack_cooldown == 0):
            if player.alive:
                pass
            ##################################################
            ######################################
            ####################################


    def update(self, player:Player.Player):
        if (self.alive):
            self.move(player.get_rect().center)

    def move(self, player_pos:tuple[int,int]):  #CENTER of player rect
        dx = player_pos[0] - self.get_rect().centerx
        dy = player_pos[1] - self.get_rect().centery
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 0.25: return
        checked_move = super().move((
            dx/distance * self.speed, 
            dy/distance * self.speed
        ))
        self.normalizeMove(checked_move)

class MeleeEnemy(Enemy):
    def __init__(self, folder:str, map, size, pos, health:int, attack_damage:int, speed:float = SETTINGS.ENEMY_DEFAULT_SPEED):
        super().__init__(folder, map, size, pos, health, attack_damage, speed)

    def update(self, player:Player.Player):
        if (self.alive):
            self.melee_attack(player)
            self.move(player.get_rect().center)