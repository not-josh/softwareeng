import pygame
from PlayerClass.Player import Player
from Camera import Camera
from Room import Map
import sys

# Initial variables
screen_width, screen_height = 1000, 1000
room_width, room_height = 1000, 65536
frame_rate = 60
SPRITE_SCALE = 5

FRAMES_AVG_OVER = 300 if frame_rate == 0 else frame_rate

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Room Gen / Rendering")

# Making an instance of the Player and placing them in the center of the screen
player = Player("Assets/doux.png", (24, 24), 24, 0, 0, SPRITE_SCALE)

# Making a camera that is the size of the room
camera = Camera(room_width, room_height, screen_width, screen_height)

# Making a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create map
map = Map(player)
map.fillRenderGroup()

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

	map.render_group.render(screen, camera)

	# Refresh (or else the old stuff stays)
	pygame.display.flip()
	
	

	f = (f + 1) % FRAMES_AVG_OVER
	# Cap frame rate
	ft = clock.tick(frame_rate)
	if (frame_rate):
		if (ft > 1 + 1000 / frame_rate): print("Single Frame: %d ms" % (ft))
	else:
		if (ft > 5): print("Single Frame: %d ms" % (ft))
	
	tft += ft
	if not f:
		if (frame_rate):
			print("%3.2f / %3.2f (ms/frame)" % (tft / FRAMES_AVG_OVER, 1000 / frame_rate))
		else:
			print("%3.2f (ms/frame)" % (tft / FRAMES_AVG_OVER))
		tft = 0


# Quit
pygame.quit()
sys.exit()