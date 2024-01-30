import pygame
import random

# Currently only two types of buildings: Building & Emptys
BUILDING_TYPES = 2
TILE_COUNT = 16
LOOT_VALUE = 100

class Room():
	def __init__(self, number):
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
	
	def __str__(self):
		string = ""
		for tile in self.tile_list:
			string += str(tile) + "\n"
		return string



# Can have a building on either side
# Ditributes loot randomly between buildings
class Tile():
	def __init__(self, loot_value):
		type_right = random.randint(0, BUILDING_TYPES - 1)
		type_left = random.randint(0, BUILDING_TYPES - 1)
		self.street_loot = 0

		if (loot_value <= 0):
			self.building_right = Building(type_right, 0)
			self.building_left = Building(type_left, 0)
			return

		if not random.getrandbits(3): # 1 in 8 chance to place all loot in the street
			self.street_loot = loot_value
			self.building_right = Building(type_right, 0)
			self.building_left = Building(type_left, 0)
			return

		bundle_1 = random.randint(0, loot_value)
		bundle_2 = loot_value - bundle_1

		self.building_right = Building(type_right, bundle_1)
		self.building_left = Building(type_left, bundle_2)

		
		

	def __str__(self):
		return "%7s    %3s    %7s" % (self.building_left, self.street_loot, self.building_right)


class Building():
	def __init__(self, type, loot_value):
		self.loot_value = loot_value
		self.type = type
	
	def __str__(self):
		return "T" + str(self.type) + " L" + str(self.loot_value)