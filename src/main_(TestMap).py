import pygame
import sys

from Map import Map
#from Map import Player
from Map import Obj
from Camera import Camera
from MusicManager import MusicManager
import Player

PRINT_RATE = 30

# Only used to display stuff without a camera class. Should be (0,0) when camera is used. 
# DRAW_OFFSET = (200, 500)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
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

# Set up the music manager
music_manager = MusicManager()
# Songs
maingame = 'assets/music/Maingame.mp3'
menu = 'assets/music/Menu.mp3'
menuclick = 'assets/sounds/menuselect.mp3'
music_manager.play_song(menu, False, .1)

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
				# Testing of changing song and sound fx
				obj = Obj("*")
				map.spawnObjAtPlayer(obj)
			if event.key == pygame.K_p:
				music_manager.play_soundfx(menuclick, 1)
			if event.key == pygame.K_o:
				music_manager.play_song(maingame, True, 0.1)


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
	#pygame.draw.rect(screen, (0, 0, 255), camera.apply(player.rect))

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