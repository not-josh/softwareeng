import pygame

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