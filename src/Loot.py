import pygame
import Renderable
import Collision
import Player
import StaticMusicManager

import SETTINGS

class Loot(Renderable.Renderable):
    def __init__(self, pos:tuple[int, int], val:int):
        self.value:int = val
        self.folder:str = SETTINGS.LOOT_TEXTURE_FOLDER
        self.pos:tuple[int, int] = pos
        self.filepath:str = self.folder
        match(val):
            case(10):
                self.filepath += "Gold_Nugget.png"
            case(100):
                self.filepath += "Gold_Ingot.png"
            case(1000):
                self.filepath += "BlocK_Of_Gold.png"
        super().__init__(self.filepath, (100,100), pos)

    def update(self, player:Player.Player) -> bool:
        if (self.rect.colliderect(player.rect)):
            player.add_points(self.value)
            StaticMusicManager.play_soundfx("assets/sounds/loot/item_pickup.wav")
            return True
        else: return False