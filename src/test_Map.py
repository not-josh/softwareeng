import pygame
import sys

from Map import Map
from Map import Player

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Game")

# Set up colors
WHITE = (255, 255, 255)

# Set up the player
player = Player()

# Set up clock
clock = pygame.time.Clock()

map = Map(100, player)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.centerx -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.centerx += 5
    if keys[pygame.K_UP]:
        player.rect.centery -= 5
    if keys[pygame.K_DOWN]:
        player.rect.centery += 5

    # Draw everything
    screen.fill(WHITE)
    map.drawRooms(screen)
    pygame.draw.rect(screen, (0, 0, 255), player.rect)

    # Refresh the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()