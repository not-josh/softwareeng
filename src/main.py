import sys
import pygame
import Player
import Lightning

def main():
    player = Player.Player("assets/sprites/entities/players/cowboy/")

    pygame.init()
    pygame.display.init()
    window = pygame.display.set_mode((720,720))
    clock = pygame.time.Clock()
    lightning_bolt_list:list = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill((0,0,0))
        window.blit(player.surface, player.rect.topleft)
        for l in lightning_bolt_list:
            window.blit(l.surface, l.rect.topleft)
        pygame.display.update()

        player.update()
        for l in lightning_bolt_list:
            l.update(player.rect.center)

        if (pygame.key.get_pressed()[pygame.K_l]):
            lightning_bolt_list.append(Lightning.Lightning("assets/sprites/entities/enemies/lightning/"))

        if (pygame.key.get_pressed()[pygame.K_z]):
            player.add_points(10)

        if (pygame.key.get_pressed()[pygame.K_c]):
            player.inventory.add_item("Chocolate")
            print(player.inventory.items["Chocolate"])
        if (pygame.key.get_pressed()[pygame.K_v]):
            player.inventory.remove_item("Chocolate")

        if (pygame.key.get_pressed()[pygame.K_y]):
            player.inventory.remove_item("Item that does not exist")

        if (pygame.key.get_pressed()[pygame.K_g]):
            player.increase_health(5)
            print(player.health)
        if (pygame.key.get_pressed()[pygame.K_h]):
            player.lower_health(5)
            print(player.health)

        if (pygame.key.get_pressed()[pygame.K_b]):
            player.increase_max_health(5)
            print(player.max_health)
        if (pygame.key.get_pressed()[pygame.K_n]):
            player.lower_max_health(5)
            print(player.max_health)

        if (pygame.key.get_pressed()[pygame.K_TAB]):
            print("Points:      " , player.points)
            print("Health:      " , player.health)
            print("Max health:  " , player.max_health)
            print("Player is:   " , ["dead     (player cannot be resurrected)", "alive"][player.alive])
        if (pygame.key.get_pressed()[pygame.K_SPACE]):
            print("Items:")
            for item in player.inventory.items:
                print(item , ": " , str(player.inventory.items[item]))

        clock.tick(60)

if __name__ == '__main__':
    main()