import pygame
import sys

from Map import Map
from Map import Player
from Map import Obj

PRINT_RATE = 30

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD to move, press 1 to spawn object at player pos")

# Set up colors
BLACK = (20,20,20)

# Set up the player
player = Player()

# Set up clock
clock = pygame.time.Clock()

map = Map(100, player, 4)

i = PRINT_RATE

# Game loop
running = True
while running:
	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				obj = Obj("*")
				map.spawnObjAtPlayer(obj)


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
	screen.fill(BLACK)
	map.tick()
	# map.drawRooms(screen)
	pygame.draw.rect(screen, (0, 0, 255), player.rect)

	# Refresh the display
	pygame.display.flip()
	
	i -= 1
	if i < 1:
		print(map)
		i = PRINT_RATE

	# Cap the frame rate
	clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()