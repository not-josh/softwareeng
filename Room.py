import pygame
import random
import PlayerClass.Player as Player
from RenderGroup import *

# File locations of all buildings
BUILDING_FILES = [
	"Assets/temptown_building_base_1.png",
	"Assets/temptown_building_base_1.png",
	"Assets/temptown_pawn_base.png"
]

ROOF_FILES = [
	"Assets/temptown_roof_1.png",
	"Assets/temptown_roof_1.png",
	"Assets/temptown_pawn_roof.png"
]

# Size in pixels of all buildings
BUILDING_RES_X = 51
BUILDING_RES_Y = 41
BUILDING_TILE_RES_Y = 19
BUILDING_SCALE = 5
BUILDING_PORCH_RES_X = 19

PAWN_FILE = "Assets/temptown_pawn_full.png"
PAWN_ROOF_FILE = ""
PAWN_RES_X = 59
PAWN_PORCH_RES_X = 22

BUILDING_GAP = BUILDING_SCALE * 0
EMPTY_BUILDINGS = 1

TILE_COUNT = 8
ROOM_GAP = 10
TILE_WIDTH = 1000
LOOT_VALUE = TILE_COUNT*6

RENDER_DIST = 500 # Should be half of screen height
RENDER_UPDATE_RATE = 10 # How many frames need to pass before updating which tiles should be rendered
ROOM_REND_RAD = 4
ROOM_UNREND_COUNT = 28 # Number of rooms that can be unloaded but stored & returned to

ROAD_COLOR = (200, 150, 100)

	# CALCULATED CONSTANTS #

BUILDING_WIDTH = BUILDING_RES_X * BUILDING_SCALE
BUILDING_HEIGHT = BUILDING_RES_Y * BUILDING_SCALE
BUILDING_FLOOR_HEIGHT = BUILDING_TILE_RES_Y * BUILDING_SCALE
BUILDING_PORCH_WIDTH = BUILDING_PORCH_RES_X * BUILDING_SCALE

PAWN_RES_Y = BUILDING_TILE_RES_Y
PAWN_WIDTH = PAWN_RES_X * BUILDING_SCALE
PAWN_HEIGHT = PAWN_RES_Y * BUILDING_SCALE
PAWN_PORCH_WIDTH = PAWN_PORCH_RES_X

TILE_HEIGHT = BUILDING_FLOOR_HEIGHT + BUILDING_GAP
ROOM_REND_COUNT = ROOM_REND_RAD * 2
REND_CENTER_INDEX = ROOM_REND_COUNT // 2

ROOM_HEIGHT = TILE_HEIGHT * TILE_COUNT + ROOM_GAP
ROOM_WIDTH = TILE_WIDTH
ROOM_TOT_COUNT = ROOM_REND_COUNT + ROOM_UNREND_COUNT



class Map():
	def __init__(self, player: Player):
		self.room_list: list[Room] = []
		self.room_count = 0

		for i in range(0, ROOM_REND_COUNT):
			self.addRoom()
		
		self.render_start = 0 # Room furthest back that will be rendered

		self.player = player
		self.player.rect.center = (ROOM_WIDTH // 2, ROOM_REND_COUNT * ROOM_HEIGHT - ROOM_HEIGHT // 2)

		self.render_group = RenderGroup(5)
		self.render_group.addTo(player, 3)
		self.rend_update_itt = 0

	def addRoom(self):
		room = Room(self.room_count)
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
	
	def update(self):
		player_current_room = self.getPlayerRoom()
		if player_current_room > REND_CENTER_INDEX:
			self.down()
		elif player_current_room < REND_CENTER_INDEX - 1:
			self.up()
		
		if self.rend_update_itt == 0:
			self.fillRenderGroup()
		else:
			self.rend_update_itt = (self.rend_update_itt + 1) % RENDER_UPDATE_RATE


	def up(self):
		# Rendering area will extend past the room list
		if (self.render_start <= 0):
			self.addRoom()
			if (len(self.room_list) >= ROOM_TOT_COUNT):
				self.removeRoom()
		else:
			self.render_start -= 1

		self.downshift()
		self.fillRenderGroup()


	def down(self):
		# If render area is at the end of the list
		if (self.render_start + ROOM_REND_COUNT + 1) >= len(self.room_list):
			pass # Do nothing
		else:
			self.render_start += 1
			self.upshift()
			self.fillRenderGroup()


	def downshift(self):
		# Shift player down
		player_pos = self.player.rect.center
		player_pos = (player_pos[0], player_pos[1] + ROOM_HEIGHT)
		self.player.rect.center = player_pos


	def upshift(self):
			# Shift player up
			player_pos = self.player.rect.center
			player_pos = (player_pos[0], player_pos[1] - ROOM_HEIGHT)
			self.player.rect.center = player_pos


	def fillRenderGroup(self):
		self.rend_update_itt = 1
		self.render_group.clear(0)
		self.render_group.clear(1)
		self.render_group.clear(4)

		player_rect = self.player.rect

		# For every room that's potentially visible
		for i in range(0, ROOM_REND_COUNT):
			index = self.render_start + i
			room = self.room_list[index]
			room.rect.topleft = (0, i * ROOM_HEIGHT)
			room.fillRenderGroup(self.render_group, player_rect)
		


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
			self.tile_list.append(Tile(tile_loot, False))
			remaining_tiles -= 1
		
		self.tile_list.append(Tile(remaining_loot, True))
		self.rect = pygame.Rect(0,0, ROOM_WIDTH, ROOM_HEIGHT)


	def fillRenderGroup(self, render_group: RenderGroup, player_rect: pygame.Rect):
		for j in range(0, TILE_COUNT):
			tile = self.tile_list[j]
			tile.rect.topleft = (0, self.rect.topleft[1] + j * TILE_HEIGHT)
			# If within render radius, add to render list
			if (abs(tile.rect.topleft[1] - player_rect.center[1]) < RENDER_DIST + BUILDING_HEIGHT):
				tile.fillRenderGroup(render_group, player_rect)
	
	def __str__(self):
		string = ""
		for tile in self.tile_list:
			string += str(tile) + "\n"
		return string



# Can have a building on either side
# Ditributes loot randomly between buildings
class Tile(Renderable):
	image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
	image.fill(ROAD_COLOR)
	pygame.draw.line(image, (30,30,10), (0,0), (TILE_WIDTH-1,0))

	def __init__(self, loot_value, has_pawn_shop):
		super().__init__()
		type_right = random.randint(-EMPTY_BUILDINGS, len(BUILDING_FILES)-2)
		type_left = random.randint(-EMPTY_BUILDINGS, len(BUILDING_FILES)-2)
		self.total_loot = loot_value
		self.street_loot = 0

		if (has_pawn_shop):
			if (random.getrandbits(1)):
				type_left = len(BUILDING_FILES)-1
			else:
				type_right = len(BUILDING_FILES)-1

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
		
		self.rect = pygame.Rect(0,0, TILE_WIDTH, TILE_HEIGHT)

	def fillRenderGroup(self, render_group: RenderGroup, player_rect: pygame.Rect):
		render_group.addTo(self, 0)

		building_y = self.rect.topleft[1] - (BUILDING_HEIGHT - TILE_HEIGHT)

		self.building_left.rect.topleft = (0, building_y)
		self.building_right.rect.topright = (TILE_WIDTH, building_y)

		self.building_left.fillRenderGroup(render_group, player_rect)
		self.building_right.fillRenderGroup(render_group, player_rect)


	def __str__(self):
		return "%7s    %3d    %7s | T=%3d" % (self.building_left, self.street_loot, self.building_right, self.total_loot)



def fillRLImageLists(file_list: list[str], face_right_list: list[pygame.Surface], face_left_list: list[pygame.Surface]) -> None:
	for file in file_list:
		asset = pygame.image.load(file)
		res_x = asset.get_width()
		imageR = pygame.Surface((res_x, BUILDING_RES_Y), pygame.SRCALPHA)
		imageR.blit(asset, (0,0), (0, 0, res_x, BUILDING_RES_Y))
		imageR = pygame.transform.scale_by(imageR, BUILDING_SCALE)
		imageL = pygame.transform.flip(imageR, True, False)

		face_right_list.append(imageR)
		face_left_list.append(imageL)


class Building(Renderable):
	# Static building images
	buildingsFaceRight: list[pygame.Surface] = []
	buildingsFaceLeft: list[pygame.Surface] = []

	fillRLImageLists(BUILDING_FILES, buildingsFaceRight, buildingsFaceLeft)

	# Contructor (style of house), (side of street), (value of loot it contains)
	def __init__(self, type, is_on_left, loot_value):
		super().__init__()
		self.type = type
		self.faces_right = is_on_left
		self.is_not_empty: bool = (self.type >= 0)

		# If there is a structure
		if (self.is_not_empty):
			self.roof = Roof(type, is_on_left)
			if self.faces_right:
				self.image = Building.buildingsFaceRight[self.type]
			else:
				self.image = Building.buildingsFaceLeft[self.type]
			self.rect: pygame.Rect = self.image.get_rect()
		else:
			self.rect: pygame.Rect = pygame.Rect(0,0,BUILDING_WIDTH,BUILDING_HEIGHT)
		
		self.valueToLoot(loot_value)
	
	# Will eventually create loot objects and place them in random locations
	def valueToLoot(self, loot_value):
		self.loot_value = loot_value
	
	def fillRenderGroup(self, render_group: RenderGroup, player_rect):
		if (self.is_not_empty):
			render_group.addTo(self, 1)
			# Relocate roof
			if (self.faces_right):
				self.roof.rect.topright = self.rect.topright
			else:
				self.roof.rect.topleft = self.rect.topleft
			self.roof.fillRenderGroup(render_group, player_rect)
		# Add loot to render group
		
	def __str__(self):
		string = ""
		string += '#' if self.type else ' '
		string += str(self.loot_value)
		return string

class Roof(Renderable):
	# Static roof images
	roofsFaceRight: list[pygame.Surface] = []
	roofsFaceLeft: list[pygame.Surface] = []

	fillRLImageLists(ROOF_FILES, roofsFaceRight, roofsFaceLeft)

	# Contructor (style of house), (side of street), (value of loot it contains)
	def __init__(self, type, is_on_left):
		super().__init__()
		self.type = type
		self.faces_right = is_on_left
		self.image: pygame.Surface

		if (self.type >= 0):
			if self.faces_right:
				self.image = Roof.roofsFaceRight[self.type]
			else:
				self.image = Roof.roofsFaceLeft[self.type]

		self.rect: pygame.Rect = self.image.get_rect()
	
	def fillRenderGroup(self, render_group: RenderGroup, player_rect: pygame.Rect):
		if (player_rect.colliderect(self.rect)):
			pass
		else:
			render_group.addTo(self, 4)
