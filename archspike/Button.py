import pygame
import sys

pygame.init()

class Button:

    def __init__(self, x, y, image, text, font):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = text
        self.font = font
        self.text_surface = font.render(text, True, (255, 255, 255))
       # self.is_clicked = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, (self.x + ((275 - self.text_surface.get_width()) // 2), self.y + 27))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

