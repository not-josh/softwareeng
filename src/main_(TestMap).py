import pygame
import sys

from Map import Map
#from Map import Player
from Map import Obj
from Camera import Camera
import Player
from ui import UI

PRINT_RATE = 30

# Only used to display stuff without a camera class. Should be (0,0) when camera is used. 
# DRAW_OFFSET = (200, 500)

# Initialize Pygame
pygame.init()

# Initialize font(s)
pygame.font.init()
ui_font = pygame.font.Font(None, 24)

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD to move, press 1 to spawn object at player pos")

# Set up colors
BLACK = (20,20,20)
WHITE = (255, 255, 255)

# Set up the player
player = Player.Player("assets/sprites/entities/players/cowboy/")

# Create UI
ui = UI(player)

# Set up clock
clock = pygame.time.Clock()

# Set up the camera
camera = Camera(player, screen_width, screen_height)

# Pass in reference to player object, as well as the vertical render distance 
# Render distance should be set to (screen height / 2) normally
map = Map(player, screen_height // 2 + 10, 4, 60)

i = PRINT_RATE

# Game loop1
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

	"""
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
	"""
	player.update()

	#just functions for player values and stuff
	player.button_functions()

	screen.fill(BLACK)
	map.tick()
	camera.update()

	# Draw everything
	render_lists = map.getRenderObjects()

	for lst in render_lists:
		for obj in lst:
			screen.blit(obj.surface, camera.apply(obj.rect).topleft)

	screen.blit(player.surface, camera.apply(player.rect))

	# Drawing the UI last
	ui.draw(screen, ui_font, WHITE)

	# Refresh the display
	pygame.display.flip()
	
	i -= 1
	if i < 1:
		print(map.getStats())
		print()
		i = PRINT_RATE

	# Cap the frame rate
	clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()