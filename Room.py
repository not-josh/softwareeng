import pygame
import random

# Currently only two types of buildings: Building & Emptys
BUILDING_TYPES = 5
TILE_COUNT = 32
LOOT_VALUE = TILE_COUNT*6

# These may become class parameters later on
TILE_HEIGHT = 64
TILE_WIDTH = 1000
BUILDING_WIDTH = 192
BUILDING_MAX_HEIGHT = TILE_HEIGHT - 4
BUILDING_PORCH_WIDTH = 64


class Room():
	def __init__(self, total_loot = LOOT_VALUE):
		self.tile_list: list[Tile] = []
		remaining_loot = total_loot
		
		# Generate tiles white distributing loot
		remaining_tiles = TILE_COUNT - 1
		while remaining_tiles > 0:
			tile_loot = 0
			# Get loot for the tile
			bitsX2 = random.getrandbits(4)
			if bitsX2 & 0b0011: 
				l = remaining_loot // remaining_tiles
				remaining_loot -= l
				tile_loot += l
			if not bitsX2 & 0b1110: 
				l = min(remaining_loot, 2 * remaining_loot // remaining_tiles)
				remaining_loot -= l
				tile_loot += l

			# Create tile
			self.tile_list.append(Tile(tile_loot))
			remaining_tiles -= 1
		
		self.tile_list.append(Tile(remaining_loot))

		# self.updateImage()


	def updateImage(self) -> pygame.Surface:
		image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT * TILE_COUNT))
		image.fill((80, 80, 80, 255))
		for i in range(0, TILE_COUNT):
			self.tile_list[i].updateImage()
			image.blit(self.tile_list[i].image, (0, TILE_HEIGHT * i))
		self.image = image

	
	def __str__(self):
		string = ""
		for tile in self.tile_list:
			string += str(tile) + "\n"
		return string



# Can have a building on either side
# Ditributes loot randomly between buildings
class Tile():
	def __init__(self, loot_value):
		self.image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
		type_right = 1 #random.randint(0, BUILDING_TYPES - 1)
		type_left = 1 #random.randint(0, BUILDING_TYPES - 1)
		self.total_loot = loot_value
		self.street_loot = 0

		if (loot_value <= 0):
			self.building_right = Building(type_right, False, 0)
			self.building_left = Building(type_left, True, 0)
		elif not random.getrandbits(3): # 1 in 8 chance to place all loot in the street
			self.street_loot = loot_value
			self.building_right = Building(type_right, False, 0)
			self.building_left = Building(type_left, True, 0)
		else:
			bundle_1 = random.randint(0, loot_value)
			bundle_2 = loot_value - bundle_1

			self.building_right = Building(type_right, False, bundle_1)
			self.building_left = Building(type_left, True, bundle_2)
		# self.updateImage()

	def updateImage(self):
		self.image.fill((0,0,0,0))
		self.building_left.updateImage()
		self.building_right.updateImage()
		self.image.blit(self.building_left.image, (0,0))
		self.image.blit(self.building_right.image, (TILE_WIDTH - BUILDING_WIDTH, 0))
		# Draw street loot
		if (self.street_loot):
			pygame.draw.circle(self.image, (0,0,0), (TILE_WIDTH//2, TILE_HEIGHT//2), 4*(self.street_loot**0.5))

	def __str__(self):
		return "%7s    %3d    %7s | T=%3d" % (self.building_left, self.street_loot, self.building_right, self.total_loot)


class Building():
	# Static building images
	building: list[pygame.Surface] = []
	for i in range(0, BUILDING_TYPES):
		building.append(pygame.Surface((BUILDING_WIDTH, BUILDING_MAX_HEIGHT), pygame.SRCALPHA))
	for i in range(1, BUILDING_TYPES):
		building[i].fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

	# Contructor (style of house), (side of street), (value of loot it contains)
	def __init__(self, type, is_on_left, loot_value):
		self.valueToLoot(loot_value)
		self.type = type
		self.faces_right = is_on_left
		# self.updateImage()
	
	# Will eventually create loot objects and place them in random locations
	def valueToLoot(self, loot_value):
		self.loot_value = loot_value

	def updateImage(self):
		self.image = pygame.Surface((BUILDING_WIDTH, BUILDING_MAX_HEIGHT), pygame.SRCALPHA)
		# If there is a building to be drawn
		if (self.type != 0):
			self.image.blit(Building.building[self.type], (0,0))
			# If the building need to face right, flip
			if (self.faces_right):
				pygame.transform.flip(self.image, True, False)
		
		self.drawLoot()
		# Draw porch roof

	# Just draws a circle on the center of the porch for now
	def drawLoot(self):
		y = BUILDING_MAX_HEIGHT // 2
		if (self.faces_right):
			x = BUILDING_WIDTH - BUILDING_PORCH_WIDTH // 2
		else:
			x = BUILDING_PORCH_WIDTH // 2
		pygame.draw.circle(self.image, (0,0,0), (x, y), 4*(self.loot_value**0.5))

		
	def __str__(self):
		string = ""
		string += '#' if self.type else ' '
		string += str(self.loot_value)
		return string