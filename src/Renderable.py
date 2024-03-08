import pygame

class Renderable(pygame.sprite.Sprite):
	surface = pygame.Surface((50,50))
	surface.fill((255,100,100))
	
	def __init__(self, texture = 0, size = 0, pos = 0):
		if texture != 0:
			self.surface = pygame.transform.scale(pygame.image.load(texture),size)
			self.__rect = self.surface.get_rect()
			# vv Note that the rectangle's TOP LEFT is set at the given coords. It's possible this
			# vv												   could need to be changed later.
			if pos: self._x, self._y = pos[0], pos[1]
			else: self._x, self._y = 0, 0
			
			if size: self.size = size
			else: self.size = (0,0)
				
			#   We could end up not needing the mask, or the mask might be better off created in the subclasses
			self.mask = pygame.mask.from_surface(self.surface)
		else:
			self.surface = Renderable.surface
			self._x, self._y = 0, 0
			self.__rect = pygame.Rect(0,0,0,0)

	# Moves without any checks of any kind. Increments x/y, recomputes rect.center
	def move(self, move:tuple[int,int]):
		self._x += move[0]
		self._y += move[1]
		self.__rect.center = (round(self._x), round(self._y))

	# If you need the get the entire rect, use *.get_rect(), but you won't be able to modify this rect
	def get_rect(self): return self.__rect
	def set_rect(self, new:pygame.Rect):
		self.__rect = new
		self._x, self._y  =  new.centerx, new.centery 
	
	# BEGIN PROPERTIES AND SETTERS
			
	# Properties and settings allow you to direction modify attributes and have it recompute related ones
	# E.g. "obj.x += 5.3" will increment obj.x and recompute the location of obj.__rect
	#	Get/set center positon:	(*.pos, *.x/y, *.center[pos but rounded])
	#	Get/set edge:			(*.left, *.bottom...)
	#	Get/set corner: 		(*.topleft, *.topright...)
	#	Get/set size: 			(*.size) - Keeps the rect centered on player's x/y
			
	@property
	def pos(self): return (self._x, self._y)
	@pos.setter
	def pos(self, set:tuple[float,float]):
		self._x, self._y = set[0], set[1]
		self.__rect.center = (round(set[0]), round(set[1]))
			
	@property
	def center(self): return (self.__rect.centerx, self.__rect.centery)
	@center.setter
	def center(self, set:tuple[int,int]): self.pos(set)
	
	@property
	def x(self): return self._x
	@x.setter
	def x(self, set):
		self._x = set
		self.__rect.centerx = round(set)
	
	@property
	def y(self): return self._y
	@y.setter
	def y(self, set):
		self._y = set
		self.__rect.centery = round(set)
	
	@property
	def size(self): return self.__rect.size
	@size.setter
	def size(self, set:tuple[int,int]):
		self.__rect.size = set
		self.__rect.center = (round(self._x), round(self._y))

	@property
	def left(self): return self.__rect.left
	@left.setter
	def left(self, set:int):
		self.__rect.left = set
		self._x = self.__rect.centerx
	
	@property
	def right(self): return self.__rect.right
	@right.setter
	def right(self, set):
		self.__rect.right = set
		self._x = self.__rect.centerx
	
	@property
	def top(self): return self.__rect.top
	@top.setter
	def top(self, set):
		self.__rect.top = set
		self._y = self.__rect.centery
	
	@property
	def bottom(self): return self.__rect.bottom
	@bottom.setter
	def bottom(self, set):
		self.__rect.bottom = set
		self._y = self.__rect.centery
	
	@property
	def topleft(self): return self.__rect.topleft
	@topleft.setter
	def topleft(self, set:tuple[int,int]):
		self.__rect.topleft = set
		self._x, self._y = self.__rect.centerx, self.__rect.centery
	
	@property
	def topright(self): return self.__rect.topright
	@topright.setter
	def topright(self, set:tuple[int,int]):
		self.__rect.topright = set
		self._x, self._y = self.__rect.centerx, self.__rect.centery
	
	@property
	def bottomleft(self): return self.__rect.bottomleft
	@bottomleft.setter
	def bottomleft(self, set:tuple[int,int]):
		self.__rect.bottomleft = set
		self._x, self._y = self.__rect.centerx, self.__rect.centery
	
	@property
	def bottomright(self): return self.__rect.bottomright
	@bottomright.setter
	def bottomright(self, set:tuple[int,int]):
		self.__rect.bottomright = set
		self._x, self._y = self.__rect.centerx, self.__rect.centery

	# END PROPERTIES AND SETTERS