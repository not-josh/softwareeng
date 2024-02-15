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
    if (pygame.key.get_pressed()[pygame.K_c]):
        player.inventory.add_item("Chocolate")
        print(player.inventory.items["Chocolate"])

    if (pygame.key.get_pressed()[pygame.K_v]):
        try:
            player.inventory.remove_item("Vanilla")     #this stuff can be ignored i was just figuring out
        except :                                        #how to manage exceptions in python
            print("a")

    clock.tick(60)
    