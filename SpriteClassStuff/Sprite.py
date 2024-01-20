import pygame

class sprite():
	def __init__(self, file: str, RES: tuple[int, int], FRAME_COUNT: int, scale = 1):
		self.RES = RES
		self.FRAME_COUNT = FRAME_COUNT
		self.spriteFrames: list = []
		self.animations: list = []
		self.currentAni: int = -1

		self.size: tuple[int, int] = (RES[0] * scale, RES[1] * scale)

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

	# Scales based on the current size (e.g. addscale(3), addscale(2) -> addscale(6))
	def addscale(self, scale: int): 
		self.size: tuple[int, int] = (self.size[0] * scale, self.size[1] * scale)
		for i in range(0, len(self.spriteFrames)): 
			self.spriteFrames[i] = pygame.transform.scale(self.spriteFrames[i], self.size)

	# Scales from the original resoltion (e.g. rescale(3), rescale(2) -> rescale(2))
	def rescale(self, scale: int): 
		self.size: tuple[int, int] = (self.RES[0] * scale, self.RES[1] * scale)
		for i in range(0, len(self.spriteFrames)): 
			self.spriteFrames[i] = pygame.transform.scale(self.spriteFrames[i], self.size)

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
	
	def getFrame(self, frameNum: int = 0):
		return self.spriteFrames[frameNum]
	
	def getFrame(self):
		if not (0 <= self.currentAni < len(self.animations)):
			return self.spriteFrames[0]
		currentAnimation = self.animations[self.currentAni]
		currentAnimation.frame()
		return self.spriteFrames[currentAnimation.fullFrame]

class animation():
	def __init__(self, RANGE: tuple[int, int], FRAME_RATIO = 1):
		self.RANGE = RANGE
		self.FRAME_RATIO = FRAME_RATIO
		self.fullFrame = RANGE[0]
		self.subFrame = 0
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