import pygame
import SETTINGS
import Renderable
import math
import Collision
from Collision import StaticCollidable

class Entity(Renderable.Renderable):
    def __init__(self, texture, size, pos, health, speed):
        super().__init__(   texture,      size,  pos)
        #                   ^ img file                  ^ size      ^start pos
        self.speed = speed
        self.health:int = health
        self.max_health = health
        self.alive = True
        self._x:float = pos[0]
        self._y:float = pos[1]

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
        self.max_health = max(1, self.max_health)
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

    # If an entity has moved too much, undo part of that move so that the entity hasn't gone past its max speed
    # I.e. normalizes movement vector to the entity's length 
    def normalizeMove(self, move):
        dist = math.sqrt(move[0]*move[0] + move[1]*move[1])
        if dist <= 1: return

        self.raw_move((
            self.speed * move[0] / dist - move[0],
            self.speed * move[1] / dist - move[1]
        ))




# For entities that walk around on the ground. 
# They can face is the 4 cardinal direcitons, and need to check collisions with the map. 
class GroundEntity(Entity):
    def __init__(self, texture_folder, map, size, pos, health, speed):
        super().__init__(texture_folder+"down.png", size, pos, health, speed)
        self.texture_folder = texture_folder
        self.map:StaticCollidable = map
        self.direction_y = "down"
    
    # Checks collisions, moves, and returns the movement vector
    # UNNORMALIZED - Does not check if the movement vector exceeds the max speed
    def move(self, move) -> tuple[float, float]:
        # Get initial position
        ini_rect = self.get_rect()
        ini_pos = (self.x, self.y)

        # Move without checks
        self.raw_move(move)

        # If vertical movement is more than horizontal
        if (abs(move[1]) > abs(move[0])+0.25): # +0.25 is to prevent spazzing when moving perfectly diagonal
            if move[1] > 0:
                self.surface = pygame.image.load(self.texture_folder + "down.png")
            else:
                self.surface = pygame.image.load(self.texture_folder + "up.png")
        else:
            if move[0] > 0:
                self.surface = pygame.image.load(self.texture_folder + "right.png")
            else:
                self.surface = pygame.image.load(self.texture_folder + "left.png")

        # Check movement and snap positon back as needed
        Collision.collision_oob_snap(self, (SETTINGS.WR_WIDTH, SETTINGS.WR_WIDTH))
        self.map.collide_stop(self, ini_rect)

        # Return movement vector
        return (self.x-ini_pos[0], self.y-ini_pos[1])
    