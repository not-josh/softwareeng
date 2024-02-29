import pygame

class Renderable(pygame.sprite.Sprite):
	surface = pygame.Surface((50,50))
	surface.fill((255,100,100))
	
	def __init__(self, texture = 0, size = 0, pos = 0):
		if texture != 0:
			self.surface = pygame.transform.scale(pygame.image.load(texture),size)
			self.rect = self.surface.get_rect()
			self.size = size
			# vv Note that the rectangle's TOP LEFT is set at the given coords. It's possible this
			# vv												   could need to be changed later.
			self.rect.topleft = pos
			#   We could end up not needing the mask, or the mask might be better off created in the subclasses
			self.mask = pygame.mask.from_surface(self.surface)
		else:
			self.surface = Renderable.surface
			self.rect = (0,0,0,0)