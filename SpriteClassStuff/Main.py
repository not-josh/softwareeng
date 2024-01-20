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
SPRITE_COUNT = 5


WALK_SPEED = 8

WIDTH = 1280
HEIGHT = 720
MAX_FPS = 60
	### End of constants ###


	### Setup ###
pygame.init()
pygame.display.set_caption("Number keys to change sprites, WASD to move, LSHIFT to change animation")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_list = []

for i in range(0, SPRITE_COUNT):
	sprite_list.append(douxSprite("Assets\\doux.png", SPRITE_SCALE))

currentSprite = 0
aniCount = douxSprite.getAniCount()

clock = pygame.time.Clock()
ft = 0 # Time since last frame (ms)

keys = pygame.key.get_pressed()

running = True
mouseClicks = (0, 0, 0)
	### End of setup ###

# WASD
def moveSprites():
	if keys[pygame.K_w]:
		sprite_list[currentSprite].pos[1] -= WALK_SPEED
	if keys[pygame.K_a]:
		sprite_list[currentSprite].pos[0] -= WALK_SPEED
	if keys[pygame.K_s]:
		sprite_list[currentSprite].pos[1] += WALK_SPEED
	if keys[pygame.K_d]:
		sprite_list[currentSprite].pos[0] += WALK_SPEED


while running:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False # Quit game
		
		if event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			# Change current sprite
			for i in range(pygame.K_0, pygame.K_0 + SPRITE_COUNT + 1):
				if keys[i]:
					currentSprite = i - pygame.K_0 - 1
					print(currentSprite)
			# Change animation
			if keys[pygame.K_LSHIFT]:
				sprite_list[currentSprite].setAnimation((sprite_list[currentSprite].currentAni + 1) % aniCount)
		
		if event.type == pygame.KEYUP:
			keys = pygame.key.get_pressed()
		
		if event.type == pygame.MOUSEBUTTONDOWN:	
			for i in range(0, SPRITE_COUNT): 
				if sprite_list[i].isClicked(pygame.mouse.get_pos()):
					print("Sprite %d clicked" % (i))
	
	moveSprites()

	# Clear screen
	screen.fill(COLOR_BG)

	# Draw onto screen
	for i in range(0, SPRITE_COUNT): 
		screen.blit(sprite_list[i].getFrame(), sprite_list[i].pos)
	
	pygame.display.flip()

	ft = clock.tick(MAX_FPS) # Limit fps
	#print("Frametime = ", ft)
	
pygame.quit()