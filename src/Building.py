import pygame
from Renderable import Renderable
from pygame import Rect
from pygame import Surface

# 	Note for future: According to pygame's documentation, running surface.convert() can optimize surfaces
# for your hardware, but only works once you have a display initialized. It may be a good idea to have a
# static method "initalizeSurfaces()" that is called after a display is initialized, but that would 
# complicate things slightly so I won't do that for now. 


BUILDINGS_DIRECTORY = "assets/sprites/buildings/"
BUILDING_VARIENTS = [
	"Generic_1/",
]


def initializeSurfaces(file_list:list[str], list_fleft:list[tuple], list_fright:list[tuple]):
	list_fleft = []
	list_fright = []
	file_count = len(file_list)

	for subdir in BUILDING_VARIENTS:
		fulldir = BUILDINGS_DIRECTORY + subdir
		fleft_entry = (Surface,) * file_count
		fright_entry = (Surface,) * file_count

		for i in range(0, file_count):
			file = file_list[i]
			surface_fleft = pygame.image.load(fulldir + file)
			surface_fleft = surface_fleft.convert()

			fleft_entry[i] = surface_fleft
			fright_entry[i] = pygame.transform.flip(list_fleft, True, False)
		
		list_fleft.append(fleft_entry)
		list_fright.append(fright_entry)


class Building(Renderable):
	# Lists for building surfaces facing left & right: [(main_base, main_roof), (...)...]
	surfaces_face_left:list[tuple[Surface, Surface]] = []
	surfaces_face_right:list[tuple[Surface, Surface]] = []


	def __init__(self, type:int, facing_left:bool) -> None:
		super().__init__()

	def initializeSurfaces():
		
		initializeSurfaces(["main_base.png", "main_roof.png"], 
					Building.surfaces_face_left, Building.surfaces_face_right)
		
		Porch.initializeSurfaces()



class Porch(Renderable):
	# Lists for building surfaces facing left & right: [(porch_base, porch_roof), (...)...]
	surfaces_face_left:list[tuple[Surface, Surface]] = []
	surfaces_face_right:list[tuple[Surface, Surface]] = []

	
	def __init__(self, type:int, facing_left:bool) -> None:
		super().__init__()
		self.facing_left = facing_left
		if (facing_left):
			self.surface = 
	
	def initializeSurfaces():
		initializeSurfaces(["porch_base.png", "porch_roof.png"], 
					Porch.surfaces_face_left, Porch.surfaces_face_right)
