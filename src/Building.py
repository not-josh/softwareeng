import pygame
from Renderable import Renderable
from pygame import Rect
from pygame import Surface

#	Current risk: Buildings and porches require multiple surfaces, which may make rendering a 
# bit more complicated. Shouldn't affect hitbox-related things like collisions. Will likely need a 
# proper "Render Group" and rendering functionality. 

TILE_HEIGHT = 120 # Will depend on height of building assets later

BUILDINGS_DIRECTORY = "assets/sprites/buildings/"
BUILDING_VARIENTS = [
	"Generic_1/"
]


def initializeSurfaces(file_list:list[str], list_fright:list[list], list_fleft:list[list]):
	list_fright.clear()
	list_fleft.clear()

	for subdir in BUILDING_VARIENTS:
		fulldir = BUILDINGS_DIRECTORY + subdir
		fright_entry = []
		fleft_entry = []

		for file in file_list:
			surface_fright = pygame.image.load(fulldir + file)
			surface_fright = pygame.transform.scale_by(surface_fright, 5) # TEMPORARY
			surface_fright = surface_fright.convert_alpha()

			fright_entry.append(surface_fright)
			fleft_entry.append(pygame.transform.flip(surface_fright, True, False))
		
		list_fright.append(fright_entry)
		list_fleft.append(fleft_entry)


class Building(Renderable):
	# Lists for building surfaces facing left & right: [(main_base, main_roof), (...)...]
	surfaces_face_right:list[list[Surface]] = []
	surfaces_face_left:list[list[Surface]] = []
	blank_surface = Surface((0,0), pygame.SRCALPHA)
	TILE_HEIGHT = TILE_HEIGHT
	isInitialized = False


	def __init__(self, tile_rect:Rect, type:int, facing_right:bool) -> None:
		super().__init__()
		
		if not Building.isInitialized:
			Building.initialize()
		
		# Assign surface and create rect
		if (type >= 0):
			if facing_right:
				self.surface = Building.surfaces_face_right[type][0]
			else:
				self.surface = Building.surfaces_face_left[type][0]
			self.rect = self.surface.get_rect()
		else:
			self.surface = Building.blank_surface
			self.rect = (0,0,50,TILE_HEIGHT)

		# Align rect
		if facing_right:
			self.rect.bottomleft = tile_rect.bottomleft
		else:
			self.rect.bottomright = tile_rect.bottomright

		# self.porch:Porch = Porch(self.rect, type, facing_right)


	def initialize():
		Porch.initialize()
		initializeSurfaces(["main_base.png", "main_roof.png"], 
					Building.surfaces_face_right, Building.surfaces_face_left)
		Building.isInitialized = True
		print("Initialized building: %d building types" % (len(Building.surfaces_face_left)))



class Porch(Renderable):
	# Lists for building surfaces facing left & right: [(porch_base, porch_roof), (...)...]
	surfaces_face_right:list[list[Surface]] = []
	surfaces_face_left:list[list[Surface]] = []
	blank_surface = Surface((0,0), pygame.SRCALPHA)

	
	def __init__(self, building_rect:Rect, type:int, facing_right:bool) -> None:
		super().__init__()
		self.facing_right = facing_right
	
	def initialize():
		initializeSurfaces(["porch_base.png", "porch_roof.png"], 
					Porch.surfaces_face_left, Porch.surfaces_face_right)
