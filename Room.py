import pygame
import random
import PlayerClass.Player as Player

# Currently only two types of buildings: Building & Emptys
BUILDING_TYPES = 5
TILE_COUNT = 4
LOOT_VALUE = TILE_COUNT*6

# These may become class parameters later on
TILE_HEIGHT = 64
TILE_WIDTH = 1000
BUILDING_WIDTH = 192
BUILDING_MAX_HEIGHT = TILE_HEIGHT - 4
BUILDING_PORCH_WIDTH = 64

ROOM_HEIGHT = TILE_HEIGHT * TILE_COUNT + 10
ROOM_WIDTH = TILE_WIDTH
RENDER_HEIGHT = 1000 # Should be half of screen height
ROOM_REND_RAD = 2
ROOM_REND_COUNT = ROOM_REND_RAD * 2
REND_CENTER_INDEX = ROOM_REND_COUNT // 2
ROOM_UNREND_COUNT = 10
ROOM_TOT_COUNT = ROOM_REND_COUNT + ROOM_UNREND_COUNT




# Render area:
	# Constrained to within the room list
	# When player leaves center, shifts forwards or backwards
		# When shifting forward
			# If render area passes room range, insert room at index 0
			# If room limit passed, delete last room (largest index)
				# Don't increment render_start
		# When shifting down
			# If would be out of range, don't shift
	# Render area defined as render_start (initialized at 0)


class Map():
	def __init__(self, player: Player):
		self.room_list: list[Room] = []
		self.room_count = 0

		for i in range(0, ROOM_REND_COUNT):
			self.addRoom()
		
		self.render_start = 0 # Room furthest back that will be rendered

		self.player = player
		self.player.rect.center = (ROOM_WIDTH // 2, ROOM_REND_COUNT * ROOM_HEIGHT - ROOM_HEIGHT // 2)

		self.image = pygame.Surface((ROOM_WIDTH, ROOM_HEIGHT))
		self.image.fill((255, 100, 100))

		self.render_group = pygame.sprite.Group()

	def addRoom(self):
		room = Room(self.room_count)
		room.updateImage()
		self.room_list.insert(0, room)
		self.room_count += 1

	def removeRoom(self):
		self.room_list.pop()

	# Converts on-screen y position to room index
	# **Index is based on rooms that are rendered, not actual index in the list
	def getPlayerRoom(self):
		player_pos = self.player.rect.center
		actual_rend_count = min(self.render_start + 1, ROOM_REND_COUNT)
		return player_pos[1] // ROOM_HEIGHT
	
	def updatePlayerRooms(self):
		player_current_room = self.getPlayerRoom()
		if player_current_room > REND_CENTER_INDEX:
			self.down()
		elif player_current_room < REND_CENTER_INDEX - 1:
			self.up()


	def up(self):
		# Rendering area will extend past the room list
		if (self.render_start <= 0):
			self.addRoom()
			if (len(self.room_list) >= ROOM_TOT_COUNT):
				self.removeRoom()
		else:
			self.render_start -= 1

		self.playerDownshift()
		self.updateImage()


	def playerDownshift(self):
		# Shift player down
		player_pos = self.player.rect.center
		player_pos = (player_pos[0], player_pos[1] + ROOM_HEIGHT)
		self.player.rect.center = player_pos


	def down(self):
		# If render area is at the end of the list
		if (self.render_start + ROOM_REND_COUNT + 1) >= len(self.room_list):
			# print("Skip shift")
			pass
		else:
			self.render_start += 1
			self.playerUpshift()
			self.updateImage()


	def playerUpshift(self):
			# Shift player up
			player_pos = self.player.rect.center
			player_pos = (player_pos[0], player_pos[1] - ROOM_HEIGHT)
			self.player.rect.center = player_pos

	
	# Old function for rendering, will hopefully make a faster one
	def updateImage(self):
		image = pygame.Surface((ROOM_WIDTH, ROOM_REND_COUNT * ROOM_HEIGHT))
		image.fill((30,30,30))

		print("Render from start %d: " % (self.render_start))
		for i in range(0, ROOM_REND_COUNT):
			index = self.render_start + i
			if (index >= 0):
				room = self.room_list[index]
				image.blit(room.image, (0, i * ROOM_HEIGHT))
				print("i%d - r%d" % (index, i))

		self.image = image

	# Adds tiles (& loot?) to render group (WIP)
	def render(self):
		image = pygame.Surface((ROOM_WIDTH, ROOM_REND_COUNT * ROOM_HEIGHT))
		image.fill((30,30,30))

		for i in range(0, ROOM_REND_COUNT):
			index = self.render_start + i
			room = self.room_list[index]
			image.blit(room.image, (0, i * ROOM_HEIGHT))

		self.image = image
		


class Room():
	def __init__(self, id = 0, total_loot = LOOT_VALUE):
		self.tile_list: list[Tile] = []
		remaining_loot = total_loot
		self.id = id
		
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