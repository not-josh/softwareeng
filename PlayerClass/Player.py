import pygame

# "Player" class
#	Contains sprites w/ animations
# 	Contains an inventory for loot
# 		Still needs a loot class for full functionality
# 	Able to move with WASD or arrow keys

AXE_VALUE = 15
KEY_VALUE = 5
BUY_MULTIPLIER = 2

PLAYER_SPEED = 5

class Inventory():
	def __init__(self):
		self.axe_count = 0
		self.key_count = 0
		self.scrap_value = 0
		self.coins = 0
	
	def sellAxes(self, count = 1) -> bool:
		if (self.axes < count): return False
		self.axes -= count
		self.coins += count * AXE_VALUE
		return True
	
	def sellKeys(self, count = 1) -> bool:
		if (self.keys < count): return False
		self.keys -= count
		self.coins += count * KEY_VALUE
		return True
	
	def sellScrap(self) -> bool:
		if (self.scrap_value <= 0): return False
		self.coins += self.scrap_value
		self.scrap_value = 0


class Player(pygame.sprite.Sprite):
	# SPRITE_RES = Resolution of a *single* frame of the sprite
	def __init__(self, sprite_file: str, SPRITE_RES: tuple[int, int], SPRITE_FRAME_COUNT, x, y, SCALE = 1):
		super().__init__()
		self.SPRITE_RES = SPRITE_RES
		self.SPRITE_FRAME_COUNT = max(1, SPRITE_FRAME_COUNT)
		self.SPRITE_FRAMES = []

		# Generate all frames of the sprite
		spritesheet = pygame.image.load(sprite_file)
		for i in range(0, self.SPRITE_FRAME_COUNT):
			frame = pygame.Surface(SPRITE_RES, pygame.SRCALPHA)
			# draw (sprite) on (origin of surface)  (X Start, Y Start, X length, Y length)
			frame.blit(spritesheet, (0, 0),	(self.SPRITE_RES[0] * i, 0, self.SPRITE_RES[0], self.SPRITE_RES[1]))
			if SCALE != 1: 
				frame = pygame.transform.scale(frame, (self.SPRITE_RES[0] * SCALE, self.SPRITE_RES[1] * SCALE))
			self.SPRITE_FRAMES.append(frame)

		# Create animation list
		self.ANIMATIONS: list = []
		self.ANIMATIONS.append(Animation((1, 3), 16))
		self.ANIMATIONS.append(Animation((4, 9), 8))
		self.ANIMATIONS.append(Animation((11, 12), 8))
		self.ANIMATIONS.append(Animation((14, 16), 12))
		self.ANIMATIONS.append(Animation((18, 23), 6))
		self.ANI_COUNT = len(self.ANIMATIONS)
		self.current_animation = self.ANIMATIONS[0]

		# Set the current image and rect (position)
		self.image = self.SPRITE_FRAMES[self.ANIMATIONS[0].current_frame]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	# Updates the current animation & frame
	# Run every frame	
	def update(self):
		self.move()
		if (self.current_animation.update()):
			self.image = self.SPRITE_FRAMES[self.current_animation.current_frame]
		pass

	# Sets the current animation
	def setAnimation(self, index):
		index = min(0, max(self.ANI_COUNT, index))
		self.current_animation = self.ANIMATIONS[index]

	# Updating based on inputs
	def move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.rect.x -= PLAYER_SPEED
		if keys[pygame.K_RIGHT]:
			self.rect.x += PLAYER_SPEED
		if keys[pygame.K_UP]:
			self.rect.y -= PLAYER_SPEED
		if keys[pygame.K_DOWN]:
			self.rect.y += PLAYER_SPEED


# Class for handling animations
class Animation():
	# FRAME_RANGE = Inclusive range of frame indices that are part of the animation
	# FRAME_RATIO = game_framerate / animation_framerate
	def __init__(self, FRAME_RANGE: tuple[int, int], FRAME_RATIO = 1):
		self.current_frame = FRAME_RANGE[0] # Set to first frame
		
		# If the "animation" is a single frame, much of the work can be skipped
		self.IS_ANIMATED = FRAME_RANGE[0] != FRAME_RANGE[1]
		if not self.IS_ANIMATED: return
		
		self.FRAME_RANGE = (min(FRAME_RANGE[0], FRAME_RANGE[1]), 
					  		max(FRAME_RANGE[0], FRAME_RANGE[1]))
		
		self.FRAME_RATIO = max(1, FRAME_RATIO)
		
		self.sub_frame = 0 # Will need to increment FRAME_RATIO times before current_frame increments

	# Should be run at every frame of the game
	# Returns True if the frame has changed
	def update(self) -> bool:
		if (self.IS_ANIMATED): # Skip if animation is a single frame (not animated)
			if (self.sub_frame == 0):
				self.current_frame += 1
				if self.current_frame > self.FRAME_RANGE[1]: self.current_frame = self.FRAME_RANGE[0]
			self.sub_frame = (self.sub_frame + 1) % self.FRAME_RATIO
			return True
		return False