import pygame
import sys

class UI:

    def __init__(self, current_hp, max_hp, loot) -> None:
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.loot = loot
        self.hp_text_loc = (10, 10)
        self.loot_text_loc = (10, 40)
        
    def setCurrentHP(self, new_hp):
        self.current_hp = new_hp

    def getHPText(self):
        return "HP: " + str(self.current_hp) + " / " + str(self.max_hp)
    
    def getLootText(self):
        return "Loot: " + str(self.loot)
    
    def getHPTextSurface(self, font):
        return font.render(self.getHPText(), True, (255, 255, 255))
    
    def getLootTextSurface(self, font):
        return font.render(self.getLootText(), True, (255, 255, 255))

    def incrementLoot(self, loot_to_add):
        self.loot += loot_to_add

    def decrementHP(self, hp_to_dec):
        self.current_hp -= hp_to_dec

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.current_hp > 0:
            self.decrementHP(1)
        if keys[pygame.K_TAB]:
            self.incrementLoot(1)
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def determineHearts(self):
        return self.current_hp // 10


    def drawUI(self, screen, screen_width, screen_height, font, heart, heart_rect):
        screen.blit(self.getHPTextSurface(font), self.hp_text_loc)
        for i in range(0, self.determineHearts()):
            heart_rect.topleft = (140 + i * 20, 15)
            screen.blit(heart, heart_rect)
        screen.blit(self.getLootTextSurface(font), self.loot_text_loc)
