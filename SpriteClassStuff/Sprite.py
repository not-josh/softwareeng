import pygame

# Contains
	# sprite - parent class of all sprites
		# fixedSprite - for sprites without animations
		# animatedSprite - parent class of animation sprites
			# douxSprite - class specifically for doux.png sprites
	# animation - for sprite animations


# General sprite class
class sprite():
	def __init__(self, file: str, RES: tuple[int, int], FRAME_COUNT: int, scale = 1):
		self.RES = RES
		self.FRAME_COUNT = FRAME_COUNT
		self.spriteFrames: list = []
		self.pos = [0,0]

		spritesheet = pygame.image.load(file)
		# Generates all frames of the sprite
		for frameNum in range(0, FRAME_COUNT): 
			sprite = pygame.Surface(RES, pygame.SRCALPHA) # Create surface for sprite to be drawn onto
			sprite.blit(spritesheet, (0, 0),
						(RES[0] * frameNum,		# Which frame of the sprite will be displayed
						0, RES[0], RES[1])) 	# Display the entire frame
			#sprite = pygame.transform.scale(sprite, self.size)
			self.spriteFrames.append(sprite)
		
		self.rescale(scale)
		
	# Scales from the original resoltion (e.g. rescale(3), rescale(2) -> rescale(2))
	def rescale(self, scale: int): 
		self.size: tuple[int, int] = (self.RES[0] * scale, self.RES[1] * scale)
		for i in range(0, len(self.spriteFrames)): 
			self.spriteFrames[i] = pygame.transform.scale(self.spriteFrames[i], self.size)
	
	def isHit(self, hitPos) -> bool:
		return (self.pos[0] <= hitPos[0] <= self.pos[0] + self.size[0]) \
			and (self.pos[1] <= hitPos[1] <= self.pos[1] + self.size[1])
		pass
	
	def getFrame(self, frameNumber: int): return self.spriteFrames[frameNumber]


# For sprites without animations
class fixedSprite(sprite):
	def __init__(self, file: str, RES: tuple[int, int], FRAME_COUNT: int, scale=1):
		super().__init__(file, RES, FRAME_COUNT, scale)
		self.currentFrame = 0
	
	def setFrame(self, newFrame: int): 
		if newFrame < 0: self.currentFrame = 0
		if newFrame >= self.FRAME_COUNT: self.currentFrame = self.FRAME_COUNT - 1

	def getFrame(self): return self.spriteFrames[self.currentFrame]


# For sprites with animations
class animatedSprite(sprite):
	def __init__(self, file: str, RES: tuple[int, int], FRAME_COUNT: int, scale=1):
		super().__init__(file, RES, FRAME_COUNT, scale)
		self.animations: list = []
		self.currentAni: int = -1

	def addAnimation(self, RANGE: tuple[int, int], FRAME_RATIO):
		if (RANGE[0] > RANGE[1] or RANGE[0] < 0 or RANGE[1] > self.FRAME_COUNT): 
			return
		self.animations.append(animation(RANGE, FRAME_RATIO))
		if self.currentAni == -1: 
			self.currentAni = 0
	
	def setAnimation(self, index: int):
		if 0 <= self.currentAni < len(self.animations):
			self.animations[self.currentAni].reset()
		if 0 <= index < len(self.animations):
			self.currentAni = index
	
	def getFrame(self):
		if not (0 <= self.currentAni < len(self.animations)):
			return self.spriteFrames[0]
		currentAnimation = self.animations[self.currentAni]
		currentAnimation.frame()
		return self.spriteFrames[currentAnimation.fullFrame]
	
	def getAniCount(self): return len(self.animations)


# Example using doux specifcally. Child classes will likely be less specific, e.g. "entitySprite"
# Specializing sprite types allows for functions like .idleAnimation(), .faceLeft(), etc., making
	# basic animation easier
class douxSprite(animatedSprite): 
	def __init__(self, file: str, scale=1):
		self.RES = (24, 24)
		self.FRAME_COUNT = 24
		super().__init__(file, self.RES, self.FRAME_COUNT, scale)

		self.addAnimation((1, 3), 16)
		self.addAnimation((4, 9), 8)
		self.addAnimation((11, 12), 8)
		self.addAnimation((14, 16), 12)
		self.addAnimation((18, 23), 6)

	def idleAni(self): self.currentAni = 0
	def walkAni(self): self.currentAni = 1
	def angryAni(self): self.currentAni = 2
	def hurtAni(self): self.currentAni = 3
	def sprintAni(self): self.currentAni = 4

	def getAniCount(): return 5


# Handles what frames are a part of what animations
class animation():
	def __init__(self, RANGE: tuple[int, int], FRAME_RATIO = 1):
		self.RANGE = RANGE
		self.FRAME_RATIO = FRAME_RATIO
		self.fullFrame = RANGE[0]
		self.subFrame = 0
		# Set frame ratio to 0 if there is only 1 frame or if ratio is negative
		if (RANGE[0] == RANGE[1]): self.FRAME_RATIO = 0
		if (FRAME_RATIO < 0): self.FRAME_RATIO = 0
	
	def frame(self) -> bool:
		if (self.FRAME_RATIO != 0): # If there is an animation
			self.subFrame = (self.subFrame + 1) % self.FRAME_RATIO
			if (self.subFrame == 0):
				self.fullFrame = self.fullFrame + 1
				if self.fullFrame > self.RANGE[1]: self.fullFrame = self.RANGE[0]
				return True
		return False
	
	def getFrame(self): return self.fullFrame

	def reset(self):
		self.fullFrame = self.RANGE[0]
		self.subFrame = 0