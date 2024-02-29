import pygame
from pygame import Rect
from Building import Building

from Renderable import Renderable
from Rendergroup import Rendergroup

import Collision
from Collision import StaticCollidable
from Camera import Camera
import random
import Player

#	Lower indecies for a tile or room list will always mean "earlier" components.
# I.e. if the player is moving forward, they will enter room[0], then room[1], etc.
# Consequently, higher indices mean lower (more negative) y-values. 


# 	This program uses standard pyton conventions, where a double-underscore indicates a private
# attribute / method, and single-underscore indicates protected. 
# 	This may change if it makes things less readable. 

TILE_HEIGHT = Building.TILE_HEIGHT
TILES_PER_ROOM = 5
ROOM_HEIGHT = TILE_HEIGHT * TILES_PER_ROOM
WIDTH = 800

REND_BUFF_DIST = 100

# TEMPORARY player class
#class Player():
	#def __init__(self):
		#self.rect = Rect(0,0,20,20)
		
# TEMPORARY generic object class, just for testing/debugging
class Obj():
	size = 15
	surface = pygame.Surface((size,size), pygame.SRCALPHA)
	surface.fill((255, 50, 10))
	
	def __init__(self, name, pos:tuple[int,int] = 0):
		self.name = name
		self.rect = Rect(0,0,Obj.size,Obj.size)
		if pos:
			self.rect.center = pos

	def __str__(self) -> str:
		return "*"


class Map(StaticCollidable):
	# Takes parameters: player, active area, inactive (but loaded) area
	def __init__(self, camera:Camera, render_group:Rendergroup, max_active_rooms:int = 4, max_inactive_rooms:int = 12) -> None:
		self.render_group = render_group
		self.camera = camera
		self.render_area:Rect = Rect(0, 0, camera.rect.width, camera.rect.height + 2 * TILE_HEIGHT)
		
		# Total number of rooms that have been generated
		self.__room_gen_count:int = 0

		self.__room_list:list[Room] = []
		self.__MAX_ROOM_COUNT = max_active_rooms + max_inactive_rooms

		# Active rooms are rooms that will be updated regularly and checked for interactions later on
		self.__ACTIVE_ROOM_COUNT = max(max_active_rooms, 4)
		self.__active_start_index = 0 # Indicies from (this) to (this + __ACTIVE_ROOM_COUNT) will be active
		
		# Not the exact center, but used to decide when to change the active range of rooms
		self.__ACTIVE_CENTER_OFFSET = self.__ACTIVE_ROOM_COUNT // 2
		
		# Player positioning
		start_y = -ROOM_HEIGHT // 2#(TILES_PER_ROOM * TILE_HEIGHT) // 2
		start_x = WIDTH // 2
		self.start_pos = (start_x, start_y)

		self.render_lists:list[list[Renderable]] = [[], [], [], [], []]

		# Generate all initial rooms
		for i in range(0, max_active_rooms):
			self.__addARoom()

	def setStartPosOf(self, object:Renderable):
		object.rect.center = self.start_pos


	# Adds a room to self.__room_list, removes a room if the limit is reached
	def __addARoom(self) -> None:
		# Generate room
		self.__room_gen_count += 1
		self.__room_list.append(Room(-ROOM_HEIGHT*self.__room_gen_count, self.__room_gen_count-1))
		# Delete room if list is too long (to save on memory ig)
		if (len(self.__room_list) > self.__MAX_ROOM_COUNT):
			self.__room_list.pop(0)
			self.__active_start_index -= 1


	# Tick functions are run every frame and have no parameters
	def tick(self) -> None:
		self.updateActiveRange()

		for i in range(self.__active_start_index, self.__active_start_index + self.__ACTIVE_ROOM_COUNT):
			room = self.__room_list[i]
			room.tick()
	
	# Updates self.__active_start_index, which determines the range of rooms considered active
	def updateActiveRange(self) -> None:
		p_room_index = self.getPlayerRoomIndex()
		active_center = self.__active_start_index + self.__ACTIVE_CENTER_OFFSET

		# If player is below the active center, shift active range down
		if (p_room_index < active_center-1):
			if self.__active_start_index > 0:
				self.__active_start_index -= 1
		
		# If player is above the active center, shift active range up
		elif (p_room_index > active_center):
			self.__active_start_index += 1
			last_active_index = self.__active_start_index + self.__ACTIVE_ROOM_COUNT
			# If the active range extends past the number of rooms
			if last_active_index > len(self.__room_list):
				self.__addARoom()
	
	# Returns the index of the room that the player is in
	def getPlayerRoomIndex(self) -> int:
		first_room_start_y = self.__room_list[0].rect.bottom
		index = (first_room_start_y-self.camera.target.rect.centery) // ROOM_HEIGHT
		if (index < 0): return 0
		if (index > len(self.__room_list)): return len(self.__room_list) - 1
		return index

	# Returns a rect that contains the entire active area of the map
	def getActiveArea(self) -> Rect:
		lowest_room = self.__room_list[0]
		highest_room = self.__room_list[self.__active_start_index + self.__ACTIVE_ROOM_COUNT + 1]
		
		left = 0
		top = highest_room.rect.top
		width = WIDTH
		height = top - lowest_room.rect.bottom
		
		return Rect(left, top, width, height)

	# Returns the rect of the room the player is approaching
	def getApproachingArea(self) -> Rect:
		approaching_room = self.__room_list[self.__active_start_index + self.__ACTIVE_ROOM_COUNT + 1]
		return approaching_room.rect

	# Spawns the object at the player's current position
	def spawnObjAtPlayer(self, obj:Obj):
		obj.rect.center = self.camera.target.rect.centery
		room = self.__room_list[self.getPlayerRoomIndex()]
		room.addObj(obj)

	def getRenderObjects(self) -> list[list[Renderable]]:
		for list in self.render_lists:
			list.clear()

		self.render_area.centery = self.camera.target.rect.centery + TILE_HEIGHT
		if (self.render_area.bottom > 0):
			self.render_area.bottom = 0

		for i in range(self.__active_start_index+self.__ACTIVE_ROOM_COUNT-1, self.__active_start_index-1, -1):
			room = self.__room_list[i]
			if room.rect.colliderect(self.render_area):
				self.render_lists[1].append(room)
				room.addRenderObjects(self.render_lists, self.render_area)
		return self.render_lists

	def fillRendergroup(self, render_group:Rendergroup = 0):
		if render_group == 0: render_group = self.render_group
		
		render_group.clearAll()

		self.render_area.centery = self.camera.target.rect.centery + TILE_HEIGHT
		if (self.render_area.bottom > 0):
			self.render_area.bottom = 0

		for i in range(self.__active_start_index+self.__ACTIVE_ROOM_COUNT-1, self.__active_start_index-1, -1):
			room = self.__room_list[i]
			if room.rect.colliderect(self.render_area):
				room.fillRenderGroup(render_group, self.render_area)

	def getStats(self) -> str:
		string = ""
		player_room_number = self.__room_gen_count - (len(self.__room_list) - self.getPlayerRoomIndex())
		topleft = self.__room_list[len(self.__room_list) - 1].rect.topleft
		bottomright = self.__room_list[0].rect.bottomright
		string += "Player room number = %d\n" % (player_room_number)
		string += "Total rooms generated = %d\n" % (self.__room_gen_count)
		player_pos = self.camera.target.rect
		string += "Camera position (x,y) = (%d,%d)\n" % (player_pos.centerx, player_pos.centery)
		string += "Map coordniate range (topleft) ~ (bottomright) = (%d,%d) ~ (%d,%d)"\
			% (topleft[0], topleft[1], bottomright[0], bottomright[1])
		return string
	
	def collide_stop(self, moving_object:Renderable, move:tuple[int,int], clear_roofs:bool = False) -> tuple[int,int]:
		for i in range(self.__active_start_index, self.__active_start_index + self.__ACTIVE_ROOM_COUNT):
			room = self.__room_list[i]
			move = room.collide_stop(moving_object, move)
		return move
	
	def playerCheck(self, player_rect:Rect):
		for i in range(self.__active_start_index, self.__active_start_index + self.__ACTIVE_ROOM_COUNT):
			room = self.__room_list[i]
			if room.rect.top - TILE_HEIGHT < player_rect.top \
				or room.rect.bottom + TILE_HEIGHT > player_rect.bottom:
				room.playerCheck(player_rect)
		pass

	# String conversion used for debugging when rendering can't be done
	def __str__(self) -> str:
		string:str = "\nActive Rooms:\n"
		for i in range(self.__active_start_index, self.__active_start_index + self.__ACTIVE_ROOM_COUNT):
			room = self.__room_list[i]
			string += room.__str__() + "\n"
		player_pos = self.camera.target.rect
		string += "Player in %d (%d, %d)" % (self.getPlayerRoomIndex(), player_pos.centerx, player_pos.centery)
		return string


class Room(StaticCollidable):
	surface = pygame.Surface((WIDTH, 1))
	surface.fill((200,200,200))

	# Parameters: room width, position (top y-value), tile count, tile height
	def __init__(self, top_y:int, id:int, tile_count:int = TILES_PER_ROOM, tile_height:int = TILE_HEIGHT) -> None:
		self.ID = id # Mostly used for debugging
		
		# Define position and size of room
		self.rect = Rect(0, top_y, WIDTH, tile_height * tile_count)

		self.tile_list:list[Tile] = []

		tile_y = self.rect.bottom
		for i in range(0, tile_count):
			tile_y -= TILE_HEIGHT
			tile = Tile(tile_y)
			self.tile_list.append(tile)
			pass
	
	# Tick functions are run every frame and have no parameters
	def tick(self):
		pass

	def __str__(self) -> str:
		string = "ID: %d (y : %d ~ %d)" % (self.ID, self.rect.bottom, self.rect.top)
		for tile in self.tile_list:
			string += "\n\t" + tile.__str__()
		return string

	# Returns the tile that collides with the center of the given rectangle
	def getTileIndexAtLoc(self, rect:Rect):
		index = (self.rect.bottom-rect.centery) // TILE_HEIGHT
		if (index < 0): return 0
		if (index > len(self.tile_list)): return len(self.tile_list)-1
		return index
	

	# Adds the given object to the tile that matches its position
	def addObj(self, obj:Obj):
		tile = self.tile_list[self.getTileIndexAtLoc(obj.rect)]
		tile.addObj(obj)

	def addRenderObjects(self, render_lists:list[list[Renderable]], render_area:Rect):
		for i in range(len(self.tile_list)-1, -1, -1):
			tile = self.tile_list[i]
			if render_area.colliderect(tile.rect):
				render_lists[0].append(tile)
				tile.addRenderObjects(render_lists)
	
	def fillRenderGroup(self, render_group:Rendergroup, render_area:Rect):
		for i in range(len(self.tile_list)-1, -1, -1):
			tile = self.tile_list[i]
			if render_area.colliderect(tile.rect):
				tile.fillRenderGroup(render_group)
		render_group.appendGround(self)
	
	def playerCheck(self, player_rect:Rect):
		for tile in self.tile_list:
			if tile.rect.top - TILE_HEIGHT < player_rect.top \
				or tile.rect.bottom + TILE_HEIGHT > player_rect.bottom:
				tile.playerCheck(player_rect)

	def collide_stop(self, moving_object:Renderable, move:tuple[int,int]) -> tuple[int,int]:
		for tile in self.tile_list:
			if tile.rect.top - TILE_HEIGHT < moving_object.rect.top \
				or tile.rect.bottom + TILE_HEIGHT > moving_object.rect.bottom:
				move = tile.collide_stop(moving_object, move)
		return move


class Tile(StaticCollidable):
	surface = pygame.Surface((WIDTH, TILE_HEIGHT))
	surface.fill((100, 50, 10))
	pygame.draw.line(surface, (0,0,0), surface.get_rect().topleft, surface.get_rect().topright)

	def __init__(self, top_y:int):
		self.rect = Rect(0, top_y, WIDTH, TILE_HEIGHT)
		self.obj_list:list[Obj] = []

		self.building_left = Building(self.rect, random.randint(-1, Building.TYPE_COUNT-1), True)
		self.building_right = Building(self.rect, random.randint(-1, Building.TYPE_COUNT-1), False)
	
	def addObj(self, obj:Obj):
		if obj.rect.colliderect(self.rect):
			self.obj_list.append(obj)
	
	def __str__(self) -> str:
		string = "(y : %d ~ %d) [" % (self.rect.bottom, self.rect.top)
		for obj in self.obj_list:
			string += obj.__str__()
		string += "]"
		return string
	
	def addRenderObjects(self, render_lists:list[list[Renderable]]):
		for obj in self.obj_list:
			render_lists[3].append(obj)
		
		self.building_left.addRenderObjects(render_lists)
		self.building_right.addRenderObjects(render_lists)

	def fillRenderGroup(self, render_group:Rendergroup):
		render_group.appendGround(self)
		for obj in self.obj_list:
			render_group.appendObject(obj)
		
		self.building_left.fillRenderGroup(render_group)
		self.building_right.fillRenderGroup(render_group)
	
	def playerCheck(self, player_rect:Rect):
		self.building_left.playerCheck(player_rect)
		self.building_right.playerCheck(player_rect)
	
	def collide_stop(self, moving_object:Renderable, move:tuple[int,int]) -> tuple[int,int]:
		move = self.building_left.collide_stop(moving_object, move)
		move = self.building_right.collide_stop(moving_object, move)
		return move