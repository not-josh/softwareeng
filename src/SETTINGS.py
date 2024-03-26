WIDTH = 800
HEIGHT = 720
FRAMERATE = 60
LOOT_TEXTURE_FOLDER = "assets/sprites/loot/"

MAX_LOOT_PER_ROOM = 8
COIN_PICKUP_SOUND = "assets/sounds/loot/item_pickup.wav"


# Might not get used in the final version, I just wanted to be able to hear my music when testing lmao
VOL_SFX = .1
VOL_MUSIC = .1


# World gen settings
WR_WIDTH = 200
WR_HEIGHT = round(WR_WIDTH * (HEIGHT / WIDTH))
WR_TILE_COUNT = 8
WR_TILE_HEIGHT = 100

LOOT_SIZE_SMALL = (8,8)
LOOT_SIZE_MEDIUM = (16,16)
LOOT_SIZE_LARGE = (10,10)