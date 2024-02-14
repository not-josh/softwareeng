import pygame
import random
from RenderGroup import *
from RenderGroup import RenderGroup
import Player

SPRITE_SCALE = 2

COIN_FILE = AXE_FILE = KEY_FILE = SCRAP_FILE = "Assets/1_coin.png"

AXE_VALUE = 15
KEY_VALUE = 10

def generateSprite(sprite_file: str) -> pygame.Surface:
	asset = pygame.image.load(sprite_file)
	size = (asset.get_width(), asset.get_height())
	sprite = pygame.Surface(size, pygame.SRCALPHA)
	sprite.blit(asset, (0,0))
	sprite = pygame.transform.scale_by(sprite, SPRITE_SCALE)
	return sprite

class Loot(Renderable):
	coin_sprite = generateSprite(COIN_FILE)
	axe_sprite = generateSprite(AXE_FILE)
	key_sprite = generateSprite(KEY_FILE)
	scrap_sprite = generateSprite(SCRAP_FILE)

	COIN = 0
	AXE = 1
	KEY = 2
	SCRAP = 3

	def __init__(self, value):
		super().__init__()
		self.image: pygame.Surface = Loot.coin_sprite
		self.value = value
		self.rect = self.image.get_rect()
	
	def appendToRenderGroup(self, render_group: RenderGroup, player_rect: pygame.Rect):
		render_group.addTo(self, 2)
	
	# If the player is colliding with loot, pickup loot
	def pickup(self, player: Player) -> bool:
		if (self.rect.colliderect(player.rect)):
			player.inventory.coin_count += self.value
			return True
		return False
