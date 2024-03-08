import pygame
import Entity
import Inventory
import math
import Collision
from Collision import StaticCollidable
import SETTINGS

class Player(Entity.Entity):# pygame.sprite.Sprite):
    def __init__(self, texture:str, map = 0):
        super().__init__(   texture+"down.png",    (100,100),  (400,400),  100,    5)
        #                   ^ img file  ^ size      ^start pos  ^health ^speed
        self.points = 0 #probably best to store points/money directly, rather than in inventory
        self.inventory = Inventory.Inventory()
        self.map:StaticCollidable = map
        self.build = 0
        self.texture_folder = texture
        self.direction_y = "down"
    
    def add_points(self, amount:int):
        if (amount < 0):
            raise Exception("Tried to add a negative amount of points")
        else:
            self.points += amount

    def remove_points(self, amount:int):
        if (amount < 0):
            raise Exception("Tried to remove a negative amount of points. Input a positive number of points to be removed.")
        else:
            self.points -= amount

    def set_points(self, points:int):
        self.points = points

    def set_points_increase_only(self, points:int):
        if (points > self.points):
            self.points = points
    
    def update(self):
        if (self.alive):
            self.move()

    def move(self):
        move = [0,0]
        horizontal_direction = 0    #   These keep track of horizontal and vertical direction. Left and down are -1,
        vertical_direction = 0      #   right and up are +1. These are used for changing direction image and for normalizing movement
        if (pygame.key.get_pressed()[pygame.K_a]):
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

        #if self.map:
        move = self.map.collide_stop(self, move)

        move = Collision.collision_oob(self, (SETTINGS.WIDTH, SETTINGS.HEIGHT), move)

        if (move[0] != 0) and (move[1] != 0):
            adjusted_speed = math.sqrt((self.speed*self.speed)/2) - 1
            move[0] = math.ceil(adjusted_speed * horizontal_direction)
            move[1] = math.ceil(adjusted_speed * vertical_direction)
            adjusted_speed = math.sqrt((self.speed*self.speed)/2)
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
                self.direction_y = "up"
            case(1):
                self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "down.png"),self.size)
                self.direction_y = "down"
        


        self.rect = self.rect.move(move)
        #   ^^ this part can basically just be sent and cleaned into a collision function in the future, but that would
        #       maybe require a reference to the map or collision masks to be sent here?






    def button_functions(self):
        if (pygame.key.get_pressed()[pygame.K_z]):
            self.add_points(10)
            print(self.points)
        if (pygame.key.get_pressed()[pygame.K_x]):
            self.remove_points(10)
            print(self.points)
        if (pygame.key.get_pressed()[pygame.K_c]):
            self.inventory.add_item("Chocolate")
            print(self.inventory.items["Chocolate"])
        if (pygame.key.get_pressed()[pygame.K_v]):
            self.inventory.remove_item("Chocolate")

        if (pygame.key.get_pressed()[pygame.K_y]):
            self.inventory.remove_item("Item that does not exist")

        if (pygame.key.get_pressed()[pygame.K_g]):
            self.increase_health(5)
            print(self.health)
        if (pygame.key.get_pressed()[pygame.K_h]):
            self.lower_health(1)
            print(self.health)

        if (pygame.key.get_pressed()[pygame.K_b]):
            self.increase_max_health(5)
            print(self.max_health)
        if (pygame.key.get_pressed()[pygame.K_n]):
            self.lower_max_health(5)
            print(self.max_health)

        if (pygame.key.get_pressed()[pygame.K_TAB]):
            print("Points:      " , self.points)
            print("Health:      " , self.health)
            print("Max health:  " , self.max_health)
            print("Player is:   " , ["dead     (player cannot be resurrected)", "alive"][self.alive])
        if (pygame.key.get_pressed()[pygame.K_SPACE]):
            print("Items:")
            for item in self.inventory.items:
                print(item , ": " , str(self.inventory.items[item]))