import pygame

class UI:

    black = (0, 0, 0)

    def __init__(self, current_hp, max_hp) -> None:
        self.current_hp = current_hp
        self.max_hp = max_hp
        

    def setCurrentHP(self, new_hp):
        self.current_hp = new_hp

    def getHPText(self):
        return "HP: " + str(self.current_hp) + " / " + str(self.max_hp)
    
    def getTextSurface(self, font):
        return font.render(self.getHPText(), True, (0, 0, 0))

    def drawUI(self, screen, screen_width, screen_height, font):
        #screen.blit(self.getTextSurface(font), ((screen_width - self.getTextSurface(font).get_width()) // 2, (screen_height - self.getTextSurface(font).get_height()) // 2))
        screen.blit(self.getTextSurface(font), (10, 10))
        #return self.font.render(self.getHPText(self), True, (255, 255, 255))
