import pygame
import random

# Currently only two types of buildings: Building & Emptys
BUILDING_TYPES = 2
TILE_COUNT = 16
LOOT_VALUE = 100

# These may become class parameters later on
TILE_HEIGHT = 96
TILE_WIDTH = 800
BUILDING_MAX_HEIGHT = TILE_HEIGHT * 2
BUILDING_WIDTH = 192
BUILDING_PORCH_WIDTH = 64

BORDER_SIZE = 200 # for testing

class Room():
	def __init__(self):
		self.tile_list: list[Tile] = []
		remaining_loot = LOOT_VALUE
		
		# Generate tiles
		remaining_tiles = TILE_COUNT - 1
		while remaining_tiles > 0:
			tile_loot = 0
			if random.getrandbits(2):
				tile_loot = remaining_loot // remaining_tiles
				remaining_loot -= tile_loot
			self.tile_list.append(Tile(tile_loot))
			remaining_tiles -= 1
		self.tile_list.append(Tile(remaining_loot))


	def getFullImage(self) -> pygame.Surface:
		image = pygame.Surface((TILE_WIDTH + BORDER_SIZE * 2, TILE_HEIGHT * TILE_COUNT + BORDER_SIZE * 2))
		image.fill((80, 80, 80, 255))
		for i in range(0, TILE_COUNT):
			image.blit(self.tile_list[i].image, (BORDER_SIZE, TILE_HEIGHT * i + BORDER_SIZE))
		return image

	
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
		type_right = random.randint(0, BUILDING_TYPES - 1)
		type_left = random.randint(0, BUILDING_TYPES - 1)
		self.total_loot = loot_value
		self.street_loot = 0

		if (loot_value <= 0):
			self.building_right = Building(type_right, 0)
			self.building_left = Building(type_left, 0)
		elif not random.getrandbits(3): # 1 in 8 chance to place all loot in the street
			self.street_loot = loot_value
			self.building_right = Building(type_right, 0)
			self.building_left = Building(type_left, 0)
		else:
			bundle_1 = random.randint(0, loot_value)
			bundle_2 = loot_value - bundle_1

			self.building_right = Building(type_right, bundle_1)
			self.building_left = Building(type_left, bundle_2)

		self.update()

	def update(self):
		self.image.fill((0,0,0,0))
		self.image.blit(self.building_left.image, (0,0))
		self.image.blit(self.building_right.image, (TILE_WIDTH - BUILDING_WIDTH, 0))
		# Draw street loot
		if (self.street_loot):
			pygame.draw.circle(self.image, (0,0,0), (TILE_WIDTH//2, TILE_HEIGHT//2), 10)

	def __str__(self):
		return "%7s    %3d    %7s | T=%3d" % (self.building_left, self.street_loot, self.building_right, self.total_loot)


class Building():
	# Static building images
	building: list[pygame.Surface] = []
	for i in range(0, BUILDING_TYPES):
		building.append(pygame.Surface((BUILDING_WIDTH, BUILDING_MAX_HEIGHT), pygame.SRCALPHA))
	for i in range(1, BUILDING_TYPES):
		building[i].fill((200, random.randint(0, 255), 15, 200))

	def __init__(self, type, loot_value):
		self.valueToLoot(loot_value)
		self.type = type
		self.update()
	
	# Placeholder funciton
	# Will eventually create loot objects and place them in random locations
	def valueToLoot(self, total_value):
		self.loot_value = total_value

	def update(self):
		self.image = pygame.Surface((BUILDING_MAX_HEIGHT, BUILDING_WIDTH), pygame.SRCALPHA)
		self.image.blit(Building.building[self.type], (0,0))
		# Draw loot
		pygame.draw.circle(self.image, (0,0,0), ((BUILDING_WIDTH + BUILDING_PORCH_WIDTH // 2), BUILDING_MAX_HEIGHT - (TILE_HEIGHT // 2)), 100)
		# Draw porch roof
	
	def __str__(self):
		string = ""
		string += '#' if self.type == 1 else ' '
		string += str(self.loot_value)
		return string