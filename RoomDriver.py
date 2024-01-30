import pygame
from PlayerClass.Player import *
from Camera import Camera
import Room
import sys

# Initial variables
screen_width, screen_height = 1000, 720
room_width, room_height = 3000, 3000
frame_rate = 60
SPRITE_SCALE = 5

room = Room.Room()

print(room)

background_image = room.getFullImage()
background_rect = background_image.get_rect()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Player Class Testing")

# Making an instance of the Player and placing them in the center of the screen
player = Player("Assets/doux.png", (24, 24), 24, screen_width // 2, screen_width // 2, SPRITE_SCALE)

# Making a camera that is the size of the room
camera = Camera(room_width, room_height, screen_width, screen_height)

# Making a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Starting the game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update calls for objects (aka: ticking)
    player.update()
    camera.update(player)

    # Draw calls for objects (aka: rendering)
    
    screen.fill((0,0,0))

    # Drawing the background
    screen.blit(background_image, camera.apply(background_rect))

    # Drawing all objects that we added to all_sprites
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    # Refresh (or else the old stuff stays)
    pygame.display.flip()

    # Cap frame rate
    ft = clock.tick(frame_rate)


# Quit
pygame.quit()
sys.exit()