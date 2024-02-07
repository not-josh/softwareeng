import pygame
def collision_stop(mask1, mask2, offset, move):
    if (mask1.overlap(mask2, (offset[0] + move[0],offset[1]))):
        move[0] = 0
    if (mask1.overlap(mask2, (offset[0], offset[1] + move[1]))):
        move[1] = 0
    if (mask1.overlap(mask2, (offset[0] + move[0], offset[1] + move[1]))):
        move[0] = 0
        move[1] = 0
    return move