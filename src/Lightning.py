import pygame
import Entity
import math
import Collision
class Lightning(Entity.Entity):
    def __init__(self, texture:str):
        super().__init__(   texture,    (100,100),  (400,400),  100,    5)
        #                   ^ img file  ^ size      ^start pos  ^health ^speed

    def update(self, player_pos:tuple[int,int]):
        self.move(player_pos)

    def move(self, player_pos:tuple[int,int]):
        move = [0,0]
        horizontal_direction = 0    #   These keep track of horizontal and vertical direction. Left and down are -1,
        vertical_direction = 0      #   right and up are +1. These are used for changing direction image and for normalizing movement
        if (player_pos):
            move[0] -= self.speed
            horizontal_direction -= 1
        if (pygame.key.get_pressed()[pygame.K_d]):
            move[0] += self.speed
            horizontal_direction += 1
        if (pygame.key.get_pressed()[pygame.K_w]):
            move[1] -= self.speed
            vertical_direction -= 1
        if (pygame.key.get_pressed()[pygame.K_s]):
            move[1] += self.speed
            vertical_direction += 1

        if (move[0] != 0) and (move[1] != 0):
            adjusted_speed = math.sqrt((self.speed*self.speed)/2) - 1
            move[0] = adjusted_speed * horizontal_direction
            move[1] = adjusted_speed * vertical_direction
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

        move = Collision.collision_oob(self, (720, 720), move)

        self.rect.left += move[0]
        self.rect.top += move[1]
        #   ^^ this part can basically just be sent and cleaned into a collision function in the future, but that would
        #       maybe require a reference to the map or collision masks to be sent here?