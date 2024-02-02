import pygame
import Camera


# Dummy simple class to declare something "renderable"
class Renderable():
	image = 0
	
	def __init__(self):
		self.pos = (0,0)


class RenderGroup():
	def __init__(self, initialize_count):
		self.super_list: list[list] = []
		for i in range(0, initialize_count):
			self.super_list.append([])
		
	def addTo(self, obj: Renderable, super_index):
		if super_index in range(0, len(self.super_list)):
			self.super_list[super_index].append(obj)
	
	def render(self, screen: pygame.Surface, camera: Camera):
		for l in self.super_list:
			for rendable in l:
				screen.blit(rendable.image, camera.apply(rendable.pos))

	def clear(self):
		for l in self.super_list:
			l.clear()