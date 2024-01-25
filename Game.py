import pygame
from Player import Player
from Camera import Camera
import sys

# Initial variables
screen_width, screen_height = 800, 800
camera_width, camera_height = 800, 800
room_width, room_height = 800, 800
frame_rate = 60

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lightning Bolt Town")

# Setting the background to an image jpg
background_image = pygame.image.load("Assets/temptown2.png")  # Replace with your image file path
background_image = pygame.transform.scale(background_image, (room_width, room_height))  # Adjust the size according to your map size
background_rect = background_image.get_rect()

#Get collision mask stuff from collision map of background
collision = pygame.image.load("Assets/temptown2_collisionmap.png")
collision = pygame.transform.scale(collision, (room_width, room_height))
#collision_rect = collision.get_rect() this was in the tutorial i used but i dont think it's ever actually used
collision_mask = pygame.mask.from_surface(collision)
collision_mask_image = collision_mask.to_surface()


# Making an instance of the Player and placing them in the center of the screen
player = Player(camera_width // 2, camera_height // 2)
player_mask = pygame.mask.from_surface(player.image)

# Making a camera that is the size of the room
camera = Camera(room_width, room_height, screen_width, screen_height)

# Making a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Starting the game loop
clock = pygame.time.Clock()
running = True

while running:


    # Update calls for objects (aka: ticking)

    #get x and y coord changes movement
    move = player.get_pos_change()
    print(move)

    #if the x change would cause an overlap, set it to 0
    if (collision_mask.overlap(player_mask, (player.rect.x + move[0],player.rect.y + 0))):
        move[0] = 0
    #if the y change would cause an overlap, set it to 0
    if (collision_mask.overlap(player_mask, (player.rect.x + 0, player.rect.y + move[1]))):
        move[1] = 0
    #send the cleaned movement coords to player.update
    player.update(move)
    camera.update(player)

    # Draw calls for objects (aka: rendering)

    # Drawing the background
    screen.blit(background_image, camera.apply(background_rect))

    #comment this line out to make collision map invisible
    screen.blit(collision, camera.apply(background_rect))

    # Drawing all objects that we added to all_sprites
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Refresh (or else the old stuff stays)
    pygame.display.flip()

    # Cap frame rate
    clock.tick(frame_rate)


# Quit
pygame.quit()
sys.exit()