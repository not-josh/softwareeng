import pygame
import Renderable

#Standard (ugly) collision function using masks
def collision_stop(mask1:pygame.mask.Mask, mask2:pygame.mask.Mask,
                   mask1_coords:tuple[int,int], mask2_coords:tuple[int,int],
                   movement:tuple[int,int]):
    x_diff = mask2_coords[0] - mask1_coords[0]
    y_diff = mask2_coords[1] - mask1_coords[1]
    if (mask1.overlap(mask2, (x_diff + movement[0], y_diff))):
        movement[0] = 0
    if (mask1.overlap(mask2, (x_diff, y_diff + movement[1]))):
        movement[1] = 0
    if (mask1.overlap(mask2, (x_diff + movement[0], y_diff + movement[1]))):
        movement = (0,0)
    return movement

    # vv refined version for Renderables, you only have to send in the objects and the movement of object2
def collision_stop(obj1:Renderable.Renderable, obj2:Renderable.Renderable,
                   movement:tuple[int,int]):
    x_diff = obj2.rect.left - obj1.rect.left
    y_diff = obj2.rect.top - obj1.rect.top
    if (obj1.mask.overlap(obj2.mask, (x_diff + movement[0], y_diff))):
        movement[0] = 0
    if (obj1.mask.overlap(obj2.mask, (x_diff, y_diff + movement[1]))):
        movement[1] = 0
    if (obj1.mask.overlap(obj2.mask, (x_diff + movement[0], y_diff + movement[1]))):
        movement = (0,0)
    return movement

#Block going out of bounds, send in player, screen size, and player's desired movement
def collision_oob(obj1:Renderable.Renderable, screen_size:tuple[int,int],
                   movement:tuple[int,int]):
    if ((obj1.rect.left + movement[0] < 0) or (obj1.rect.right + movement[0] >= screen_size[0])):
        movement[0] = 0
    if (obj1.rect.bottom + movement[1] > 0):
        movement[1] = 0
    #if (obj1.rect.bottom + movement[1] >= screen_size[1]):
    #    movement[1] = 0
    return movement

#Rect version of collision
def collision_stop(rect1:pygame.rect.Rect, rect2:pygame.rect.Rect,
                   movement:tuple[int,int]):
    if (rect1.colliderect(rect2.move(movement[0],0))):
        movement[0] = 0
    if (rect1.colliderect(rect2.move(0,movement[1]))):
        movement[1] = 0
    #if (mask1.overlap(mask2, (x_diff, y_diff + movement[1]))):
    #    movement[1] = 0
    #if (mask1.overlap(mask2, (x_diff + movement[0], y_diff + movement[1]))):
    #    movement = (0,0)
    return movement


# Class for non-moving objects that are collidable
# Needed to prevent circular imports between Player and Map
class StaticCollidable():
    rect = pygame.Rect(0,0,0,0)
    
    def collide_stop(self, object:Renderable):
        pass