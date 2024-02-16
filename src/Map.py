import pygame

# 	Anytime there is a list of a set number of objects equally spaced apart vertically
# they will be sorted so that lower indicies means larger y-value

# 	This program uses standard pyton conventions, where a double-underscore indicates a private
# attribute / method, and single-underscore indicates protected. This may change if the underscore
# do more harm than good, but will remain for now. 

TILE_HEIGHT = 20 # Will depend on height of building assets later
TILES_PER_ROOM = 8
ROOM_HEIGHT = TILE_HEIGHT * TILES_PER_ROOM



# TEMPORARY player class
class Player():
	def __init__(self):
		self.rect = pygame.Rect(0,0,20,20)



class Map():
	# Takes parameters: map width, player, active area, inactive (but loaded) area
	def __init__(self, width:int, player_to_follow: Player, max_active_rooms:int = 4, max_inactive_rooms:int = 32) -> None:
		self.__WIDTH = width
		
		# Total number of rooms that have been generated
		self.__room_gen_count:int = 0
		
		
		self.__room_list:list[Room] = []
		self.__MAX_ROOMS = max_active_rooms + max_inactive_rooms
		# Active rooms are rooms that will be updated regularly and checked for interactions later on
		self.__ACTIVE_ROOM_COUNT = max(max_active_rooms, 4)
		self.__active_start_index = 0 # Indicies from (this) to (this + __ACTIVE_ROOM_COUNT) will be active
		
		# Not the exact center, but used to decide when to change the active range of rooms
		self.__ACTIVE_CENTER_OFFSET = self.__ACTIVE_ROOM_COUNT // 2
		
		# Player positioning
		self.player = player_to_follow
		player_start_y = 0 #(TILES_PER_ROOM * TILE_HEIGHT) // 2
		self.player.rect.centery = player_start_y

		# Generate all initial rooms
		for i in range(0, max_active_rooms):
			self.__addARoom()


	# Adds a room to self.__room_list, removes a room if the limit is reached
	def __addARoom(self):
		self.__room_list.insert(0, Room(self.__WIDTH, ROOM_HEIGHT*self.__room_gen_count))
		if (len(self.__room_list) > self.__MAX_ROOMS):
			self.__room_list.pop()
			self.__active_start_index -= 1
		self.__room_gen_count += 1
	

	def getPlayerRoomIndex(self) -> int:
		return self.player.rect.centery // ROOM_HEIGHT + 1


	# Tick functions are run every frame and have no parameters
	def tick(self) -> None:
		p_room_index = self.getPlayerRoomIndex()

		# If player is in the lowest active room
		if (p_room_index < self.__ACTIVE_CENTER_OFFSET-1):
			if self.__active_start_index > 0:
				self.__active_start_index -= 1
		# If player is in the highest active room
		elif (p_room_index > self.__ACTIVE_CENTER_OFFSET):
			# Add any rooms if the 
			last_active_index = self.__active_start_index + self.__ACTIVE_ROOM_COUNT
			while (last_active_index >= self.__MAX_ROOMS):
				self.__addARoom()
				last_active_index = self.__active_start_index + self.__ACTIVE_ROOM_COUNT
			if last_active_index < 


		for i in range(self.__active_start_index, self.__active_start_index + self.__ACTIVE_ROOM_COUNT):
			room = self.__room_list[i]
			room.tick()
	
	def __str__(self) -> str:
		return "Room Index %d" % (self.getPlayerRoomIndex)

	def drawRooms(self, surface:pygame.Surface):
		for i in range(self.__active_start_index, self.__active_start_index + self.__ACTIVE_ROOM_COUNT):
			room = self.__room_list[i]
			room.drawRooms(surface)


class Room():
	# Parameters: room width, position (y value of top of room), tile count, tile height
	def __init__(self, width:int, top_y:int, tile_count:int = TILES_PER_ROOM, tile_height:int = TILE_HEIGHT) -> None:
		# Define position and size of room
		self.rect = pygame.Rect(0, top_y, width, tile_height * tile_count)
	
	# Tick functions are run every frame and have no parameters
	def tick(self):
		pass

	def drawRooms(self, surface:pygame.Surface):
		pygame.draw.rect(surface, (30,20,5), self.rect)