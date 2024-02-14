import sys
import pygame
import Player
player = Player.Player("assets/sprites/entities/players/cowboy.png")


pygame.init()
pygame.display.init()
window = pygame.display.set_mode((720,720))
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    window.fill((0,0,0))
    window.blit(player.surface, player.rect.topleft)
    pygame.display.update()
    player.move()
    clock.tick(60)
    