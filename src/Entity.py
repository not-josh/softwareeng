import pygame
import SETTINGS
import Renderable
import math
import Collision
from Collision import StaticCollidable

class Entity(Renderable.Renderable):
	def __init__(self, texture, size, pos, health, speed):
		super().__init__(   texture,	  size,  pos)
		#				   ^ img file				  ^ size	  ^start pos
		self.speed = speed
		self.health:int = health
		self.max_health = health
		self.alive = True
		self._x:float = pos[0]
		self._y:float = pos[1]

	def lower_health(self, value:int):
		self.health -= value
		self.health = max(0,self.health)
		if (self.health == 0):
			self.alive = False

	def increase_health(self, value:int):
		self.health += value
		self.health = min(self.health, self.max_health)

	def lower_max_health(self, decrease:int):
		self.max_health -= decrease
		self.max_health = max(1, self.max_health)
		if (self.max_health < self.health):
			self.lower_health(self.health-self.max_health)

	def increase_max_health(self, increase:int):
		old_max_health = self.max_health
		self.max_health += increase
		if (old_max_health != 0):
			self.health = int(self.health * (self.max_health / old_max_health))
	def kill(self):
		self.health = 0
		self.alive = False





class GroundEntity(Entity):
	def __init__(self, texture_folder, map, size, pos, health, speed):
		super().__init__(texture_folder+"down.png", size, pos, health, speed)
		self.map:StaticCollidable = map
		self.texture_folder = texture_folder
		self.direction_y = "down"
	
	# Checks collisions, moves, and sets animations
	def move(self, move_dir):
		move = [self.speed * move_dir[0], self.speed * move_dir[1]]

		#if self.map:
		move = self.map.collide_stop(self, move)

		move = Collision.collision_oob(self, (SETTINGS.WIDTH, SETTINGS.HEIGHT), move)

		if (move[0] != 0) and (move[1] != 0):
			adjusted_speed = math.sqrt((self.speed*self.speed)/2) - 1
			move[0] = adjusted_speed * move_dir[0]
			move[1] = adjusted_speed * move_dir[1]
			adjusted_speed = math.sqrt((self.speed*self.speed)/2)
			move[0] = adjusted_speed * move_dir[0]
			move[1] = adjusted_speed * move_dir[1]
		#   ^^ "normalizes" the movement "vector" ^^
		match(move_dir[0]):
			case(-1):
				self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "left.png"),self.size)
			case(1):
				self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "right.png"),self.size)
		match(move_dir[1]):
			case(-1):
				self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "up.png"),self.size)
				self.direction_y = "up"
			case(1):
				self.surface = pygame.transform.scale(pygame.image.load(self.texture_folder + "down.png"),self.size)
				self.direction_y = "down"
	
		self.rect = self.rect.move(move)
		  