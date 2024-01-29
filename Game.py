import pygame
from Player import Player
from Camera import Camera
import sys
from UI import UI

# Initial variables
screen_width, screen_height = 800, 800
camera_width, camera_height = 800, 800
room_width, room_height = 1600, 1600
frame_rate = 60

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()

# UI and font setup
font = pygame.font.Font(None, 36)
ui = UI(50, 50, 100)

# Sprites
heart = pygame.image.load("Assets/heart.png")
heart_rect = heart.get_rect()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lightning Bolt Town")

# Setting the background to an image jpg
background_image = pygame.image.load("Assets\Background\mudkip.jpg")  # Replace with your image file path
background_image = pygame.transform.scale(background_image, (room_width, room_height))  # Adjust the size according to your map size
background_rect = background_image.get_rect()

# Making an instance of the Player and placing them in the center of the screen
player = Player(camera_width // 2, camera_height // 2)

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
    ui.update()

    # Draw calls for objects (aka: rendering)

    # Drawing the background
    screen.blit(background_image, camera.apply(background_rect))

    # Drawing all objects that we added to all_sprites
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    # Drawing the UI
    #screen.blit(ui.drawUI(), ((screen_width - ui.drawUI().get_width()) // 2, (screen_height - ui.drawUI().get_height()) // 2))
    ui.drawUI(screen, screen_width, screen_height, font, heart, heart_rect)
    #screen.blit(text_surface, ((screen_width - text_surface.get_width()) // 2, (screen_height - text_surface.get_height()) // 2))

    # Refresh (or else the old stuff stays)
    pygame.display.flip()

    # Cap frame rate
    clock.tick(frame_rate)


# Quit
pygame.quit()
sys.exit()