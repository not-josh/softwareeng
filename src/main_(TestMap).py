import pygame
import sys

from Map import Map
from Camera import Camera
import Player
from Rendergroup import Rendergroup

FRAME_RATE = 120
PRINT_RATE = FRAME_RATE if FRAME_RATE else 600 

# Only used to display stuff without a camera class. Should be (0,0) when camera is used. 
# DRAW_OFFSET = (200, 500)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD to move, press 1 to spawn object at player pos")

# Set up colors
BG_COLOR = (255, 63, 127)

# Set up the player
player = Player.Player("assets/sprites/entities/players/cowboy/")

# Set up clock
clock = pygame.time.Clock()

# Set up the camera
camera = Camera(player, screen_width, screen_height)

render_group = Rendergroup()

# Pass in reference to player object, as well as the vertical render distance 
# Render distance should be set to (screen height / 2) normally
map = Map(camera, render_group, 4, 60)
map.setStartPosOf(player)

player.map = map

i = PRINT_RATE

# Game loop1
running = True
while running:
	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	

	player.update()
	player.button_functions() # Functions for player values
	map.tick() # Update map

	# Rendering preperations
	screen.fill(BG_COLOR) # Clear screen
	map.playerCheck(player.rect)
	camera.update()

	# Rendering
	map.fillRendergroup(render_group)
	render_group.appendTo(player, 3)
	render_group.render(screen, camera)

	# Refresh the display
	pygame.display.flip()

	# Renderng cleanup
	render_group.clearAll()
	
	i -= 1
	if i < 1:
		# print(map.getStats())
		print(clock.get_fps())
		i = PRINT_RATE

	# Cap the frame rate
	clock.tick(FRAME_RATE)

# Quit Pygame
pygame.quit()
sys.exit()