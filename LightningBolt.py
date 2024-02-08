import pygame

#class LightningTarget():
TARGET_SPEED = 3
TOTAL_TIME = 500

class LightningBolt(pygame.sprite.Sprite):
	# SPRITE_RES = Resolution of a *single* frame of the sprite
	def __init__(self, sprite_folder: str, SPRITE_RES: tuple[int, int], SPRITE_FRAME_COUNT, x, y, SCALE = 1):
		super().__init__()
		self.SPRITE_RES = SPRITE_RES
		self.SPRITE_FRAME_COUNT = max(1, SPRITE_FRAME_COUNT)
		self.SPRITE_FRAMES = []
		self.time = TOTAL_TIME
		self.sprite_folder = sprite_folder
		self.can_move = True

		# Set the current image and rect (position)
		self.image = pygame.transform.scale_by(pygame.image.load(sprite_folder + "/lightning_bolt_target.png"), SCALE)
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.center = (x, y)

	# Updates the current animation & frame
	# Run every frame	
	def update(self, movechange):
		self.time -= 1
		self.move(movechange)
				
	#Gets future position if the player is allowed to move
	def get_pos_change(self, player_pos):
		pos_change = [0,0]
		if (self.can_move == False):
			return pos_change
		else:
			if player_pos[0] < self.rect.center[0]:
				pos_change[0] -= TARGET_SPEED
			if player_pos[0] > self.rect.center[0]:
				pos_change[0] += TARGET_SPEED
			if player_pos[1] < self.rect.center[1]:
				pos_change[1] -= TARGET_SPEED
			if player_pos[1] > self.rect.center[1]:
				pos_change[1] += TARGET_SPEED
			return pos_change

	def move(self, coords):
		self.rect.x += coords[0]
		self.x += coords[0]
		self.rect.y += coords[1]
		self.y += coords[1]
		
	def strike(self):
		self.image = pygame.transform.scale_by(pygame.image.load(self.sprite_folder + "/lightning_bolt.png"), 5)
		self.rect.y -= 256
		self.can_move = False
		pygame.mixer.Sound("Assets/Sounds/weird_zap_damage.wav").play()