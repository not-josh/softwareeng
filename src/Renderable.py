import pygame

class Renderable(pygame.sprite.Sprite):
	surface = pygame.Surface((50,50))
	surface.fill((255,100,100))
	
	def __init__(self, texture = 0, size = 0, pos = 0):
		if texture != 0:
			self.surface = pygame.transform.scale(pygame.image.load(texture),size)
			self._rect = self.surface.get_rect()
			self.size = size
			# vv Note that the rectangle's TOP LEFT is set at the given coords. It's possible this
			# vv												   could need to be changed later.
			if pos:
				self._rect.topleft = pos
				self._x, self._y = pos[0], pos[1]
			else:
				self._x, self._y = 0, 0
			#   We could end up not needing the mask, or the mask might be better off created in the subclasses
			self.mask = pygame.mask.from_surface(self.surface)
		else:
			self.surface = Renderable.surface
			self._rect = (0,0,0,0)
	
	# BEGIN PROPERTIES AND SETTERS
	@property
	def left(self): return self._rect.left
	@left.setter
	def left(self, set:int):
		self._rect.left = set
		self._x = self._rect.centerx
	
	@property
	def right(self): return self._rect.right
	@right.setter
	def right(self, set):
		self._rect.right = set
		self._x = self._rect.centerx
	
	@property
	def top(self): return self._rect.top
	@top.setter
	def top(self, set):
		self._rect.top = set
		self._y = self._rect.centery
	
	@property
	def bottom(self): return self._rect.bottom
	@bottom.setter
	def bottom(self, set):
		self._rect.bottom = set
		self._y = self._rect.centery
	
	@property
	def topleft(self): return self._rect.topleft
	@topleft.setter
	def topleft(self, set:tuple[int,int]):
		self._rect.topleft = set
		self._x, self._y = self._rect.centerx[0], self._rect.centery[1]
	
	@property
	def topright(self): return self._rect.topright
	@topright.setter
	def topright(self, set:tuple[int,int]):
		self._rect.topright = set
		self._x, self._y = self._rect.centerx[0], self._rect.centery[1]
	
	@property
	def bottomleft(self): return self._rect.bottomleft
	@bottomleft.setter
	def bottomleft(self, set:tuple[int,int]):
		self._rect.bottomleft = set
		self._x, self._y = self._rect.centerx[0], self._rect.centery[1]
	
	@property
	def bottomright(self): return self._rect.bottomright
	@bottomright.setter
	def bottomright(self, set:tuple[int,int]):
		self._rect.bottomright = set
		self._x, self._y = self._rect.centerx[0], self._rect.centery[1]
	
	@property
	def pos(self): return (self._x, self._y)
	@pos.setter
	def pos(self, set:tuple[int,int]):
		self._x, self._y = set[0], set[1]
		self._rect.center = (round(set[0]), round(set[1]))
	
	@property
	def x(self): return self._x
	@x.setter
	def x(self, set):
		self._x = set
		self._rect.centerx = round(set)
	
	@property
	def y(self): return self._y
	@y.setter
	def y(self, set):
		self._y = set
		self._rect.centery = round(set)

	# END PROPERTIES AND SETTERS