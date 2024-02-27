import pygame
import Entity
import math
import Collision
class Lightning(Entity.Entity):
    def __init__(self, folder:str, pos:tuple[int,int]):
        super().__init__(   folder+"target.png",    (100,100),  pos,        100,    3)
        #                   ^ img file              ^ size      ^start pos  ^health ^speed
        self.folder = folder

    def update(self, player_pos:tuple[int,int]):    #player pos refers to CENTER of player rect here and in move()
        self.move(player_pos)

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

        #move = Collision.collision_oob(self, (720, 720), move)

        #newx = self.rect.centerx + move[0]
        #newy = self.rect.centery + move[1]
        #   ^^ this part can basically just be sent and cleaned into a collision function in the future, but that would
        #       maybe require a reference to the map or collision masks to be sent here?