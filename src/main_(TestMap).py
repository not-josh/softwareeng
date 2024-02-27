import pygame
import sys
import random

from Map import Map
#from Map import Player
from Map import Obj
from Camera import Camera
import Player
import Lightning

PRINT_RATE = 30

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
BLACK = (20,20,20)

# Set up the player
player = Player.Player("assets/sprites/entities/players/cowboy/")

# Set up clock
clock = pygame.time.Clock()

# Set up the camera
camera = Camera(player, screen_width, screen_height)

# Pass in reference to player object, as well as the vertical render distance 
# Render distance should be set to (screen height / 2) normally
map = Map(player, screen_height // 2 + 10, 4, 60)

lightning_bolt_list = []

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
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				obj = Obj("*")
				map.spawnObjAtPlayer(obj)

	player.update()

	#just functions for player values and stuff
	player.button_functions()

	if (pygame.key.get_pressed()[pygame.K_l]):
		if (l_pressed == False):
			newl = Lightning.Lightning("assets/sprites/entities/enemies/lightning/", (player.rect.centerx, player.rect.top-100), FRAME_RATE * 5)
			lightning_bolt_list.append(newl)
		l_pressed = True
	else:
		l_pressed = False

	if (current_frame==0):					# once per second:
		newr = random.randrange(0,10,1)		# 20% random chance to
		print(newr)
		if (newr == 0):						# spawn new lightning (with 5 second duration)
			newl = Lightning.Lightning("assets/sprites/entities/enemies/lightning/", (player.rect.centerx, player.rect.top-100), FRAME_RATE * 5)
			lightning_bolt_list.append(newl)

	screen.fill(BLACK)
	map.tick()
	camera.update()

	# Draw everything
	render_lists = map.getRenderObjects()

	render_lists

	for lst in render_lists:
		for obj in lst:
			screen.blit(obj.surface, camera.apply(obj.rect).topleft)

	screen.blit(player.surface, camera.apply(player.rect))
	#pygame.draw.rect(screen, (0, 0, 255), camera.apply(player.rect))

	for l in lightning_bolt_list:
		l.update(player)
		if (l.alive):
			screen.blit(l.surface, camera.apply(l.rect))
		else:
			lightning_bolt_list.remove(l)

	# Refresh the display
	pygame.display.flip()
	
	i -= 1
	
	if i < 1:
		#print(map.getStats())
		#print()
		i = PRINT_RATE

	current_frame += 1

	if (current_frame == FRAME_RATE):
		current_frame = 0
	

	# Cap the frame rate
	clock.tick(FRAME_RATE)

# Quit Pygame
pygame.quit()
sys.exit()