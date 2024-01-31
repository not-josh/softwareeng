import pygame
from PlayerClass.Player import *
from Camera import Camera
import Room
import sys

# Initial variables
screen_width, screen_height = 1000, 720
room_width, room_height = 1000, 8000
frame_rate = 60
SPRITE_SCALE = 5

FRAMES_AVG_OVER = 60
REGENERATE_ROOM_RATE = 10

room = Room.Room()
room.updateImage()
background_image = room.image
background_rect = background_image.get_rect()

print(room)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Room Generation Testing")

# Making an instance of the Player and placing them in the center of the screen
player = Player("Assets/doux.png", (24, 24), 24, screen_width // 2, screen_height // 2, SPRITE_SCALE)

# Making a camera that is the size of the room
camera = Camera(room_width, room_height, screen_width, screen_height)

# Making a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Starting the game loop
clock = pygame.time.Clock()
running = True

f = 0
r = 0
ft = 0
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
	
	r = (r + 1) % REGENERATE_ROOM_RATE
	if not r:
		room = Room.Room()
		room.updateImage()
		background_image = room.image
		background_rect = background_image.get_rect()
	

	f = (f + 1) % FRAMES_AVG_OVER
	# Cap frame rate
	ft += clock.tick(frame_rate)
	if not f:
		print("%3.2f (ms/frame)" % (ft / FRAMES_AVG_OVER))
		ft = 0


# Quit
pygame.quit()
sys.exit()