import pygame
import sys
import random

from Map import Map
from Camera import Camera
import Player
from Rendergroup import Rendergroup
import Lightning

FRAME_RATE = 120
PRINT_RATE = FRAME_RATE if FRAME_RATE else 600 

FRAME_RATE = 60

# Only used to display stuff without a camera class. Should be (0,0) when camera is used. 
# DRAW_OFFSET = (200, 500)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 720
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

Lightning.setMap(map)

lightning_bolt_list:list[Lightning.Lightning] = []

l_pressed = False

i = PRINT_RATE

current_frame = 0

# Game loop1
running = True
while running:
	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if (pygame.key.get_pressed()[pygame.K_l]):
		if (l_pressed == False):
			newl = Lightning.Lightning("assets/sprites/entities/enemies/lightning/", (player.rect.centerx, player.rect.top-100), FRAME_RATE * 5)
			lightning_bolt_list.append(newl)
		l_pressed = True
	else:
		l_pressed = False

	# Spawn new lightning bolts
	current_frame += 1
	if (current_frame == FRAME_RATE):	
		current_frame = 0				# once per second:
		newr = random.randrange(0,10,1)		# 20% random chance to
		if (newr == 0):						# spawn new lightning (with 5 second duration)
			newl = Lightning.Lightning("assets/sprites/entities/enemies/lightning/", (player.rect.centerx, player.rect.top-100), FRAME_RATE * 5)
			lightning_bolt_list.append(newl)
	

	# Object updates
	player.update()
	player.button_functions() # Functions for player values
	map.tick() # Update map	
	player.button_functions() #just functions for player values and stuff

	# Update lighting bolts and add them to the render group
	for l in lightning_bolt_list:
		l.update(player)
		if (l.alive):
			render_group.appendSky(l)
		else:
			lightning_bolt_list.remove(l)


	# Rendering prep
	screen.fill(BG_COLOR)
	map.playerCheck(player)
	camera.update()

	# Rendering
	map.fillRendergroup(render_group)
	render_group.appendTo(player, 3)
	render_group.render(screen, camera) # Render everything within the render group

	# Refresh the display
	pygame.display.flip()

	# Renderng cleanup
	render_group.clearAll()
	
	i -= 1
	
	if i < 1:
		# print(map.getStats())
		print(clock.get_fps())
		#print(map.getStats())
		# print("Player Health =", player.health)
		i = PRINT_RATE

	
	
	# Cap the frame rate
	clock.tick(FRAME_RATE)

# Quit Pygame
pygame.quit()
sys.exit()