import pygame
import random
import PlayerClass.Player as Player
from RenderGroup import *
from Loot import Loot


# Overview of how this works:
	# Map has Rooms
	# Room has Tiles
	# Tile has Loot and Buildings & is renderable
	# Building has Loot and Roof & is renderable
	# Roof and Loot are renderable

	# Renderable means it inherits from RenderGroup.Renderable
		# All renderable objects get added to a RenderGroup when they need to be rendered
		# Has an image and a rect (for position/size)
		# Has appendToRenderGroup(), which takes a RenderGroup, and the player's location (rect)
			# Each child's implementation can be different, but the idea is to decide how and where
			# itself and its components will be added to the RenderGroup.
			# E.g. Tile.appendToRenderGroup() repositions all of its buildings, 
			#  adds itself to the group, then calls buildings.appendToRenderGroup()

	# Each renderable object has a static list of the possible sprites that can be rendered.
	#  This prevents the need for sprites getting redrawn each time a new room is generated, 
	#  which would cause lagspikes. 

	# See RenderGroup.py for more details on Renderable/Rendegroup



# File locations of all buildings
BUILDING_FILES = [
	"Assets/temptown_building_base_1.png",
	"Assets/temptown_building_base_1.png",
	"Assets/temptown_pawn_base.png"
]

BUILDING_MASK_FILES = [
	"Assets/temptown_building_base_1_mask.png",
	"Assets/temptown_building_base_1_mask.png",
	"Assets/temptown_pawn_base_mask.png"
]

ROOF_FILES = [
	"Assets/temptown_roof_1.png",
	"Assets/temptown_roof_1.png",
	"Assets/temptown_pawn_roof.png"
]

# Size in pixels of normal buildings
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


# Holds and manages all rooms, as well as which rooms need to be rendered/updated
class Map():
	def __init__(self, player: Player):
		self.room_list: list[Room] = []
		self.room_count = 0
		self.mask = pygame.mask.Mask((0,0))
		self.rh = ROOM_HEIGHT

		for i in range(0, ROOM_REND_COUNT):
			self.addRoom()

		self.mask_img = self.mask.to_surface()


		
		self.render_start = 0 # Furthest-back room to be rendered (e.g. 1 might mean rooms 1~5 are rendered)

		self.player: Player = player
		self.player.rect.center = (ROOM_WIDTH // 2, ROOM_REND_COUNT * ROOM_HEIGHT - ROOM_HEIGHT // 2)

		self.render_group = RenderGroup(5) # Create RenderGroup with 5 render layers (layers 0~4)
		self.render_group.addTo(player, 3) # Add player to layer 3
		self.rend_update_itt = 0

	# Adds a room as the new "furthest forward" room
	def addRoom(self):
		room = Room(self.room_count)
		self.room_list.insert(0, room)
		self.room_count += 1
		self.mask.draw(room.mask, room.rect.topleft)

	# Removes the "furthest back" room
	def removeRoom(self):
		self.room_list.pop()

	# Converts on-screen y position to room index
	# **Index is based on rooms that are rendered, not actual index in the list
	def getPlayerRoom(self):
		player_pos = self.player.rect.center
		actual_rend_count = min(self.render_start + 1, ROOM_REND_COUNT)
		return player_pos[1] // ROOM_HEIGHT
	
	# Checks if the player has reached a new room and if the map needs to be shifted
	def update(self):
		self.player.update()
		ret = 0
		player_current_room = self.getPlayerRoom()
		if player_current_room > REND_CENTER_INDEX:
			ret = self.down()
		elif player_current_room < REND_CENTER_INDEX - 1:
			ret = self.up()
		
		if self.rend_update_itt == 0:
			self.fillRenderGroup()
		else:
			self.rend_update_itt = (self.rend_update_itt + 1) % RENDER_UPDATE_RATE
		return ret

	# Player moved up
	def up(self):
		# Rendering area will extend past the room list
		if (self.render_start <= 0):
			self.addRoom()
			if (len(self.room_list) >= ROOM_TOT_COUNT):
				self.removeRoom()
		else:
			self.render_start -= 1

		self.downshift() # Shift everything back down
		self.fillRenderGroup()
		return 1

	# Player moved down
	def down(self):
		# If render area is at the end of the list
		if (self.render_start + ROOM_REND_COUNT + 1) >= len(self.room_list):
			return 0 # Do nothing
		else:
			self.render_start += 1
			self.upshift() # Shift everything back up
			self.fillRenderGroup()
			return -1

	# Shift every downwards to account for player moving up too far
	def downshift(self):
		# Shift player down
		player_pos = self.player.rect.center
		player_pos = (player_pos[0], player_pos[1] + ROOM_HEIGHT)
		self.player.rect.center = player_pos

	# Shift every upwards to account for player moving down too far
	def upshift(self):
		# Shift player up
		player_pos = self.player.rect.center
		player_pos = (player_pos[0], player_pos[1] - ROOM_HEIGHT)
		self.player.rect.center = player_pos

	# Fills self.render_group with tiles/buildings/etc
	def fillRenderGroup(self,):
		self.rend_update_itt = 1
		# Clear render lists (except 3, which contains the player)
		self.render_group.clear(0)
		self.render_group.clear(1)
		self.render_group.clear(2)
		self.render_group.clear(4)

		player_rect = self.player.rect

		# For every room that's potentially visible
		for i in range(0, ROOM_REND_COUNT):
			index = self.render_start + i
			room = self.room_list[index]
			room.rect.topleft = (0, i * ROOM_HEIGHT)
			room.appendToRenderGroup(self.render_group, player_rect, self.player.mask)
	
	def checkInteractions(self): 
		for i in range(0, ROOM_REND_COUNT):
			room_index = self.render_start + i
			room = self.room_list[room_index]

			room.checkInteractions(self.player)
		

# Holds and manages a set of tiles
class Room():
	def __init__(self, id = 0, total_loot = LOOT_VALUE):
		self.tile_list: list[Tile] = []
		remaining_loot = total_loot
		self.id = id
		self.masky = 0-TILE_HEIGHT
		self.mask = pygame.mask.Mask((ROOM_WIDTH, ROOM_HEIGHT))
		self.roof_mask = pygame.mask.Mask((ROOM_WIDTH, ROOM_HEIGHT))
		
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
			newtile = Tile(tile_loot, False)
			self.tile_list.append(newtile)
			self.mask.draw(newtile.mask, (0, self.masky))
			self.roof_mask.draw(newtile.roof_mask, (0, self.masky))
			self.masky += TILE_HEIGHT
			remaining_tiles -= 1
		newpawntile = Tile(remaining_loot, True)
		self.tile_list.append(newpawntile)
		self.mask.draw(newpawntile.mask, (newpawntile.rect.topleft[0], self.masky))
		self.roof_mask.draw(newpawntile.roof_mask, (newpawntile.rect.topleft[0], self.masky))
		self.rect = pygame.Rect(0,0, ROOM_WIDTH, ROOM_HEIGHT)

		

	# Adds all of its tiles to the render group
	def appendToRenderGroup(self, render_group: RenderGroup, player_rect: pygame.Rect, player_mask):
		for j in range(0, TILE_COUNT):
			tile = self.tile_list[j]
			tile.rect.topleft = (0, self.rect.topleft[1] + j * TILE_HEIGHT)
			# If within render radius, add to render list
			if (abs(tile.rect.topleft[1] - player_rect.center[1]) < RENDER_DIST + BUILDING_HEIGHT):
				tile.appendToRenderGroup(render_group, player_rect, player_mask)
	
	def checkInteractions(self, player: Player):
		# Check interactions for this room
		for j in range(0, TILE_COUNT):
			tile = self.tile_list[j]
			tile_y = tile.rect.centery
			player_y = player.rect.centery
			if (tile_y - TILE_HEIGHT < player_y < tile_y + TILE_HEIGHT):
				tile.checkInteractions(player)



# Has a building on either side
# Ditributes loot randomly between buildings & street
class Tile(Renderable):
	image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
	image.fill(ROAD_COLOR)
	pygame.draw.line(image, (30,30,10), (0,0), (TILE_WIDTH-1,0))

	def __init__(self, loot_value, has_pawn_shop):
		super().__init__()
		type_right = random.randint(-EMPTY_BUILDINGS, len(BUILDING_FILES)-2)
		type_left = random.randint(-EMPTY_BUILDINGS, len(BUILDING_FILES)-2)
		self.total_loot = loot_value
		self.street_loot = False
		self.image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
		self.image.fill(ROAD_COLOR)
		pygame.draw.line(self.image, (30,30,10), (0,0), (TILE_WIDTH-1,0))
		self.mask = pygame.mask.Mask((TILE_WIDTH, TILE_HEIGHT*2))
		self.roof_mask = pygame.mask.Mask((TILE_WIDTH, TILE_HEIGHT*2))

		if (has_pawn_shop):
			if (random.getrandbits(1)):
				type_left = len(BUILDING_FILES)-1
			else:
				type_right = len(BUILDING_FILES)-1

		# Loot distribution
		if (loot_value <= 0):
			self.building_right = Building(type_right, False, 0)
			self.building_left = Building(type_left, True, 0)
		elif not random.getrandbits(3): # 1 in 8 chance to place all loot in the street
			self.street_loot = Loot(loot_value)
			self.building_right = Building(type_right, False, 0)
			self.building_left = Building(type_left, True, 0)
		else:
			bundle_1 = random.randint(0, loot_value)
			bundle_2 = loot_value - bundle_1

			self.building_right = Building(type_right, False, bundle_1)
			self.building_left = Building(type_left, True, bundle_2)
		
		self.rect = pygame.Rect(0,0, TILE_WIDTH, TILE_HEIGHT)
		self.mask.draw(self.building_left.mask, (0,0))
		self.mask.draw(self.building_right.mask, (TILE_WIDTH-self.building_right.rect.width, self.building_right.rect.topleft[1]))
		if (type_left >= 0):
			self.roof_mask.draw(self.building_left.roof.mask, (self.building_left.rect.width-self.building_left.roof.mask.get_size()[0],0))
		if (type_right >= 0):
			self.roof_mask.draw(self.building_right.roof.mask, (TILE_WIDTH-self.building_right.rect.width, self.building_right.rect.topleft[1]))


	# Add self and buildings to render group
	def appendToRenderGroup(self, render_group: RenderGroup, player_rect: pygame.Rect, player_mask):
		render_group.addTo(self, 0)

		building_y = self.rect.topleft[1] - (BUILDING_HEIGHT - TILE_HEIGHT)

		self.building_left.rect.topleft = (0, building_y)
		self.building_right.rect.topright = (TILE_WIDTH, building_y)

		self.building_left.appendToRenderGroup(render_group, player_rect, player_mask)
		self.building_right.appendToRenderGroup(render_group, player_rect, player_mask)

		if (self.street_loot):
			self.street_loot.rect.center = self.rect.center
			self.street_loot.appendToRenderGroup(render_group, player_rect)

	def checkInteractions(self, player: Player):
		# Check interactions for this tile
		self.building_left.checkInteractions(player)
		self.building_right.checkInteractions(player)
		pass

# Creates lists of right/left facing images from a list of files
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

# Contains loot and roofs
class Building(Renderable):
	# Static building images
	buildingsFaceRight: list[pygame.Surface] = []
	buildingsFaceLeft: list[pygame.Surface] = []

	fillRLImageLists(BUILDING_FILES, buildingsFaceRight, buildingsFaceLeft)

	buildingsMasksFaceRight: list[pygame.mask.Mask] = []
	buildingsMasksFaceLeft: list[pygame.mask.Mask] = []

	fillRLImageLists(BUILDING_MASK_FILES, buildingsMasksFaceRight, buildingsMasksFaceLeft)

	# Contructor (style of house), (side of street), (value of loot it contains)
	def __init__(self, type, is_on_left, loot_value):
		super().__init__()
		self.type = type
		self.faces_right = is_on_left
		self.is_not_empty: bool = (self.type >= 0)
		self.mask = pygame.mask.Mask((BUILDING_WIDTH, BUILDING_HEIGHT))

		# If there is a structure, create roof and set self.image
		if (self.is_not_empty):
			self.roof = Roof(type, is_on_left)
			if self.faces_right:
				self.image = Building.buildingsFaceRight[self.type]
				self.mask = pygame.mask.from_surface(Building.buildingsMasksFaceRight[self.type])
			else:
				self.image = Building.buildingsFaceLeft[self.type]
				self.mask = pygame.mask.from_surface(Building.buildingsMasksFaceLeft[self.type])
			self.rect: pygame.Rect = self.image.get_rect()
			#self.mask = pygame.mask.from_surface(self.image)
		else:
			self.rect: pygame.Rect = pygame.Rect(0,0,BUILDING_WIDTH,BUILDING_HEIGHT)
			self.roof = False
		
		self.valueToLoot(loot_value)
	
	# Basically a placeholder for more complex loot generation
	def valueToLoot(self, loot_value):
		if (loot_value >= 0):
			self.loot: Loot = Loot(loot_value)
		else:
			self.loot = False
	
	# Add self to render group, call appendToRenderGroup() on sub-components
	def appendToRenderGroup(self, render_group: RenderGroup, player_rect, player_mask):
		if (self.is_not_empty):
			render_group.addTo(self, 1)
			# Relocate roof
			if (self.faces_right):
				self.roof.rect.topright = self.rect.topright
			else:
				self.roof.rect.topleft = self.rect.topleft
			self.roof.appendToRenderGroup(render_group, player_rect, player_mask)
		if (self.loot):
			if (self.faces_right): loot_x = self.rect.topright[0] - 50
			else: loot_x = self.rect.topleft[0] + 50
			loot_y = self.rect.bottom - TILE_HEIGHT // 2 
			self.loot.rect.center = (loot_x, loot_y)
			self.loot.appendToRenderGroup(render_group, player_rect)
		
	def checkInteractions(self, player: Player):
		# Check interactions for this building
		pass


# Roof for buildings
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
		self.mask = pygame.mask.from_surface(self.image)

		if (self.type >= 0):
			if self.faces_right:
				self.image = Roof.roofsFaceRight[self.type]
			else:
				self.image = Roof.roofsFaceLeft[self.type]
		self.mask = pygame.mask.from_surface(self.image)

		self.rect: pygame.Rect = self.image.get_rect()
	
	def appendToRenderGroup(self, render_group: RenderGroup, player_rect: pygame.Rect, player_mask):
		if (player_rect.colliderect(self.rect)):
			pass
		else:
			render_group.addTo(self, 4)
