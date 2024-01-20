# Videos used in learning: 
	# Spritesheets - https://www.youtube.com/watch?v=M6e3_8LHc7A
	# Transparency - https://www.youtube.com/watch?v=8_HVdxBqJmE

# This program shows the rendering of sprites with simple animations
# Click/drag anywhere on the screen to move the sprite to your current cursor position

import pygame

	### Constants ###
COLOR_BG = (45, 25, 15)

SPRITE_RES = (24, 24)
SPRITE_SCALE = 3 		# How much the sprite will be scaled up (i.e. by a factor of 3)
SPRITE_FRAME_COUNT = 24	# Number of frames for the sprite
SPRITE_FRAME_RATIO = 8 	# How many frames need to be rendered before the sprite changes frame

WIDTH = 1280
HEIGHT = 720
MAX_FPS = 60
	### End of constants ###


	### Setup ###
pygame.init()
pygame.display.set_caption("Click/drag to move sprite to cursor")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

spritesheet = pygame.image.load("Assets\\doux.png")
spriteFrames: list = []

# Generates all frames of the sprite
for frameNum in range(0, SPRITE_FRAME_COUNT): 
	sprite = pygame.Surface(SPRITE_RES, pygame.SRCALPHA) # Create surface for sprite to be drawn onto
	sprite.blit(spritesheet, (0, 0),
				(SPRITE_RES[0] * frameNum,			# Which frame of the sprite will be displayed
				0, SPRITE_RES[0], SPRITE_RES[1])) 	# Display the entire frame
	sprite = pygame.transform.scale(sprite, (SPRITE_RES[0] * SPRITE_SCALE, SPRITE_RES[1] * SPRITE_SCALE)) # Rescale sprite
	spriteFrames.append(sprite)

clock = pygame.time.Clock()
ft = 0 # Time since last frame (ms)

currentSpriteFrame = 0
spritePos = (0,0)

running = True
mousePressed = False
	### End of setup ###


while running:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False # Quit game
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			mousePressed = True
		if event.type == pygame.MOUSEBUTTONUP:
			mousePressed = False

	# If clicking, move sprite	
	if (mousePressed): spritePos = pygame.mouse.get_pos()

	# Clear screen
	screen.fill(COLOR_BG)

	# Draw onto screen
	screen.blit(spriteFrames[(currentSpriteFrame // SPRITE_FRAME_RATIO)], spritePos)
	currentSpriteFrame = (currentSpriteFrame + 1) % (SPRITE_FRAME_COUNT * SPRITE_FRAME_RATIO)
	pygame.display.flip()

	ft = clock.tick(MAX_FPS) # Limit fps
	print("Frametime = ", ft)
	
pygame.quit()