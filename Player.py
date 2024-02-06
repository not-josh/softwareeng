import pygame

# "Player" class
#	Contains sprites w/ animations
#		All frames of a sprite are pre-calculated, e.i. loaded and drawn onto surfaces
# 	Contains an inventory for loot
# 		Should still create a separate loot class of some kind
# 	Able to move with WASD or arrow keys
#	Functions to deal damage and heal the player

AXE_VALUE = 15
KEY_VALUE = 5
BUY_MULTIPLIER = 2

PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 5


# Literally just a bunch of buy/sell functions
class Inventory():
	def __init__(self):
		self.axe_count = 0
		self.key_count = 0
		self.scrap_value = 0
		self.coin_count = 0
	
	def sellAxe(self, count = 1) -> bool:
		if (self.axes < count): return False
		self.axes -= count
		self.coin_count += count * AXE_VALUE
		return True
	
	def sellKey(self, count = 1) -> bool:
		if (self.keys < count): return False
		self.keys -= count
		self.coin_count += count * KEY_VALUE
		return True
	
	def sellScrap(self) -> bool:
		if (self.scrap_value <= 0): return False
		self.coin_count += self.scrap_value
		self.scrap_value = 0
		return True

	def sellAll(self) -> bool:
		sold_something = False
		if (self.sellAxe(self.axe_count)): sold_something = True
		if (self.sellKey(self.key_count)): sold_something = True
		if (self.sellScrap()): sold_something = True
		return sold_something

	def buyAxe(self, count = 1) -> bool:
		value = AXE_VALUE * BUY_MULTIPLIER * count
		if (self.coin_count < value): return False
		self.axes += count
		self.coin_count -= value
		return True
	
	def buyKey(self, count = 1) -> bool:
		value = KEY_VALUE * BUY_MULTIPLIER * count
		if (self.coin_count < value): return False
		self.key_count += count
		self.coin_count -= value
		return True


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
			# draw from spritesheet onto (origin of surface), piece of spritesheet = (X Start, Y Start, X length, Y length)
			frame.blit(spritesheet, (0, 0),	(self.SPRITE_RES[0] * i, 0, self.SPRITE_RES[0], self.SPRITE_RES[1]))
			if SCALE != 1: 
				frame = pygame.transform.scale(frame, (self.SPRITE_RES[0] * SCALE, self.SPRITE_RES[1] * SCALE))
			self.SPRITE_FRAMES.append(frame)

		# Create animation list
		self.ANIMATIONS = [
			Animation((1, 3), 16),
			Animation((4, 9), 8),
			Animation((11, 12), 8),
			Animation((14, 16), 12),
			Animation((18, 23), 6)
		]
		self.ANI_COUNT = len(self.ANIMATIONS)
		self.current_animation = self.ANIMATIONS[0]

		# Set the current image and rect (position)
		self.image = self.SPRITE_FRAMES[self.ANIMATIONS[0].current_frame]
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.center = (x, y)

		# Set up player stats
		self.inventory = Inventory()
		self.health = PLAYER_MAX_HEALTH

	# Updates the current animation & frame
	# Run every frame	
	def update(self, movechange):
		self.move(movechange)
		# If the animation frame has updated
		if (self.current_animation.update()):
			self.image = self.SPRITE_FRAMES[self.current_animation.current_frame]
		pass

	# Sets the current animation & reset the previous animation
	def setAnimation(self, index):
		if (0 <= index < self.ANI_COUNT):
			new_animation = self.ANIMATIONS[index]
			if (new_animation != self.current_animation):
				self.current_animation.reset()
				self.current_animation = self.ANIMATIONS[index]
				self.image = self.SPRITE_FRAMES[self.current_animation.current_frame]
				
	#Gets future position if the player is allowed to move
	def get_pos_change(self):
		pos_change = [0,0]
		ani = -1
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			pos_change[1] -= PLAYER_SPEED
			ani = 4
		if keys[pygame.K_DOWN]:
			pos_change[1] += PLAYER_SPEED
			ani = 3
		if keys[pygame.K_LEFT]:
			pos_change[0] -= PLAYER_SPEED
			ani = 0
		if keys[pygame.K_RIGHT]:
			pos_change[0] += PLAYER_SPEED
			ani = 1
		self.setAnimation(ani)
		return pos_change


	    # Updating based on inputs
	def move(self, coords):
		ani = -1
		self.rect.x += coords[0]
		self.x += coords[0]
		self.rect.y += coords[1]
		self.y += coords[1]
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_LEFT]:
        #    self.rect.x -= self.speed
        #if keys[pygame.K_RIGHT]:
        #    self.rect.x += self.speed
        #if keys[pygame.K_UP]:
        #    self.rect.y -= self.speed
        #if keys[pygame.K_DOWN]:
        #    self.rect.y += self.speed

	def isAlive(self):
		return self.health > 0
	
	def damage(self, damage):
		self.health -= damage
		
	def heal(self, heal, can_revive: bool = False): 
		if (self.isAlive() or can_revive): # If alive or can be revived
			self.health = min(self.health + heal, PLAYER_MAX_HEALTH)
		# If dead and can't revive, do nothing


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
			self.sub_frame = (self.sub_frame + 1) % self.FRAME_RATIO
			if (self.sub_frame == 0):
				self.current_frame += 1
				if self.current_frame > self.FRAME_RANGE[1]: self.current_frame = self.FRAME_RANGE[0]
				return True
		return False
	
	def reset(self):
		self.sub_frame = 0
		self.current_frame = self.FRAME_RANGE[0]