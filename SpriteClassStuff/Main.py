# Videos used in learning: 
	# Spritesheets - https://www.youtube.com/watch?v=M6e3_8LHc7A
	# Transparency - https://www.youtube.com/watch?v=8_HVdxBqJmE

# too tired to comment idk

import pygame
from Sprite import *

	### Constants ###
COLOR_BG = (45, 25, 15)

SPRITE_RES = (24, 24)
SPRITE_SCALE = 6 		# How much the sprite will be scaled up (i.e. by a factor of 3)
SPRITE_FRAME_COUNT = 24	# Number of frames for the sprite
SPRITE_FRAME_RATIO = 8 	# How many frames need to be rendered before the sprite changes frame

WALK_SPEED = 8

WIDTH = 1280
HEIGHT = 720
MAX_FPS = 60
	### End of constants ###


	### Setup ###
pygame.init()
pygame.display.set_caption("WASD & Arros to move sprites, shift keys change animations")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_1 = sprite("Assets\\doux.png", (24, 24), 24, SPRITE_SCALE)
sprite_1.addAnimation((1, 3), 16)
sprite_1.addAnimation((4, 9), 8)
sprite_1.addAnimation((11, 12), 8)
sprite_1.addAnimation((14, 16), 12)
sprite_1.addAnimation((18, 23), 6)

sprite_2 = sprite("Assets\\doux.png", (24, 24), 24, SPRITE_SCALE)
sprite_2.addAnimation((1, 3), 16)
sprite_2.addAnimation((4, 9), 8)
sprite_2.addAnimation((11, 12), 8)
sprite_2.addAnimation((14, 16), 12)
sprite_2.addAnimation((18, 23), 6)

aniCount = 5

clock = pygame.time.Clock()
ft = 0 # Time since last frame (ms)

spritePos_1 = [0, 0]
spritePos_2 = [0, 0]

keys = pygame.key.get_pressed()

running = True
mouseClicks = (0, 0, 0)
	### End of setup ###

def moveSprites():
	global keys
	oldKeys = keys
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w]:
		spritePos_1[1] -= WALK_SPEED
	if keys[pygame.K_a]:
		spritePos_1[0] -= WALK_SPEED
	if keys[pygame.K_s]:
		spritePos_1[1] += WALK_SPEED
	if keys[pygame.K_d]:
		spritePos_1[0] += WALK_SPEED
	if keys[pygame.K_LSHIFT] and not oldKeys[pygame.K_LSHIFT]:
		sprite_1.setAnimation((sprite_1.currentAni + 1) % aniCount)
		
	if keys[pygame.K_UP]:
		spritePos_2[1] -= WALK_SPEED
	if keys[pygame.K_LEFT]:
		spritePos_2[0] -= WALK_SPEED
	if keys[pygame.K_DOWN]:
		spritePos_2[1] += WALK_SPEED
	if keys[pygame.K_RIGHT]:
		spritePos_2[0] += WALK_SPEED
	if keys[pygame.K_RSHIFT] and not oldKeys[pygame.K_RSHIFT]:
		sprite_2.setAnimation((sprite_2.currentAni + 1) % aniCount)


while running:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False # Quit game

	moveSprites()

	# Clear screen
	screen.fill(COLOR_BG)

	# Draw onto screen
	screen.blit(sprite_1.getFrame(), spritePos_1)
	screen.blit(sprite_2.getFrame(), spritePos_2)
	pygame.display.flip()

	ft = clock.tick(MAX_FPS) # Limit fps
	#print("Frametime = ", ft)
	
pygame.quit()