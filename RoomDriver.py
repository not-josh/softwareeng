import pygame
from PlayerClass.Player import Player
from Camera import Camera
from Room import Map
import sys

# Initial variables
screen_width, screen_height = 1000, 720
room_width, room_height = 1000, 65536 * 16
frame_rate = 45
SPRITE_SCALE = 5

FRAMES_AVG_OVER = 600

USE_OLD_RENDERING = False

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Room Generation Testing")

# Making an instance of the Player and placing them in the center of the screen
player = Player("Assets/doux.png", (24, 24), 24, 0, 0, SPRITE_SCALE)

# Making a camera that is the size of the room
camera = Camera(room_width, room_height, screen_width, screen_height)

# Making a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create map
map = Map(player, USE_OLD_RENDERING)
map.updateImage()
map.fillRenderList()

# Starting the game loop
clock = pygame.time.Clock()
running = True

f = 0
ft = 0
tft = 0
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				print("Player is in room %d" % (map.getPlayerRoom()), map.player.rect.center)
	
	# Update calls for objects (aka: ticking)
	map.update()
	player.update()
	camera.update(player)

	# Draw calls for objects (aka: rendering)
	
	screen.fill((0,0,0))

	if (USE_OLD_RENDERING):
		screen.blit(map.image, camera.apply(map.image.get_rect()))
	else:
		tile_list = map.render_list
		for i in range(0, len(tile_list)):
			tile = tile_list[i]
			screen.blit(tile.image, camera.apply(tile.pos))

	# Drawing all objects that we added to all_sprites
	for sprite in all_sprites:
		screen.blit(sprite.image, camera.apply(sprite))

	# Refresh (or else the old stuff stays)
	pygame.display.flip()
	
	

	f = (f + 1) % FRAMES_AVG_OVER
	# Cap frame rate
	ft = clock.tick(frame_rate)
	if (ft > 2): print("Single Frame: %d ms" % (ft))
	tft += ft
	if not f:
		print("%3.2f (ms/frame)" % (tft / FRAMES_AVG_OVER))
		tft = 0


# Quit
pygame.quit()
sys.exit()