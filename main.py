import pygame, sys
from Button import Button 
from UI import UI
from Player import Player
from Camera import Camera
import random
from Coin import Coin

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")
menu_button_font = pygame.font.Font(None, 56)

# Getting assets
BG = pygame.image.load("Assets/Background/TitleScreen_bgd.png")
music_titlescreen = pygame.mixer.music.load("Assets/Music/TitleScreen.mp3")
pygame.mixer.music.set_volume(0.25)

frame_rate = 60

white_blank_menu = pygame.image.load("Assets/Menu/White_Blank.png")
red_blank_menu = pygame.image.load("Assets/Menu/Red_Blank.png")

white_blank_menu = pygame.transform.scale(white_blank_menu, (int(white_blank_menu.get_width() * 2.5), int(white_blank_menu.get_height() * 2.5)))
red_blank_menu = pygame.transform.scale(red_blank_menu, (int(red_blank_menu.get_width() * 2.5), int(red_blank_menu.get_height() * 2.5)))

play_button = Button(250, 300, white_blank_menu, "Play", menu_button_font)
options_button = Button(250, play_button.y + 150, white_blank_menu, "Options", menu_button_font)
quit_button = Button(250, options_button.y + 150, white_blank_menu, "Quit", menu_button_font)

menu_buttons = [play_button, options_button, quit_button]

# Playing the title screen music
pygame.mixer.music.play(-1)

def get_font(size):
    pass

def play():
    pygame.display.set_caption("Play")

    # Initial variables
    screen_width, screen_height = 800, 800
    camera_width, camera_height = 800, 800
    room_width, room_height = 800, 800
    frame_rate = 60

    while True:
        SPRITE_SCALE = 5

        # Colors
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)

        pygame.init()

        # UI and font setup
        font = pygame.font.Font(None, 36)
        ui = UI(50, 50, 100)

        # Sprites
        heart = pygame.image.load("Assets/heart.png")
        heart_rect = heart.get_rect()

        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Lightning Bolt Town")

        # Setting the background to an image jpg
        background_image = pygame.image.load("Assets/temptown2.png")  # Replace with your image file path
        background_image = pygame.transform.scale(background_image, (room_width, room_height))  # Adjust the size according to your map size
        background_rect = background_image.get_rect()

        # Setting the foreground to an image jpg
        foreground_image = pygame.image.load("Assets/temptown2_roofs.png")  # Replace with your image file path
        foreground_image = pygame.transform.scale(foreground_image, (room_width, room_height))  # Adjust the size according to your map size
        foreground_rect = foreground_image.get_rect()

        #Get collision mask stuff from collision map of background
        collision = pygame.image.load("Assets/temptown2_collisionmap.png")
        collision = pygame.transform.scale(collision, (room_width, room_height))
        #collision_rect = collision.get_rect() this was in the tutorial i used but i dont think it's ever actually used
        collision_mask = pygame.mask.from_surface(collision)
        collision_mask_image = collision_mask.to_surface()

        # Making an instance of the Player and placing them in the center of the screen
        player = Player("Assets/doux.png", (24, 24), 24, screen_width // 2, screen_width // 2, SPRITE_SCALE)
        player_mask = pygame.mask.from_surface(player.image)

        # Making a camera that is the size of the room
        camera = Camera(room_width, room_height, screen_width, screen_height)

        # Making a sprite group
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        coins = []
        coin_x = 0
        coin_y = 0
        num_remaining_coins = random.randint(0,5)
        print("Number of coins: ", num_remaining_coins)
        while num_remaining_coins > 0:# a in range (0, 100):#num_coins):
            coin_x = random.randint(0, screen_width)
            coin_y = random.randint(0, screen_height)
            newc = Coin(coin_x, coin_y)
            if not (collision_mask.overlap(newc.mask, (newc.rect.x, newc.rect.y))):
                coins.append(newc)
                all_sprites.add(newc)
                num_remaining_coins -= 1

        print(len(coins))
            

        # Starting the game loop
        clock = pygame.time.Clock()
        running = True

        active_collision = False
        x_collision = False
        y_collision = False
        thud = pygame.mixer.Sound("Assets/Sounds/big_thud.wav")

        while running:


            # Update calls for objects (aka: ticking)

            #get x and y coord changes movement
            move = player.get_pos_change()
            if move[0] != 0 or move[1] !=0:
                # print(move)

                #if the x change would cause an overlap, set it to 0
                if (collision_mask.overlap(player_mask, (player.rect.x + move[0],player.rect.y + 0))):
                    move[0] = 0
                    x_collision = True
                else:
                    x_collision = False
                #if the y change would cause an overlap, set it to 0
                if (collision_mask.overlap(player_mask, (player.rect.x + 0, player.rect.y + move[1]))):
                    move[1] = 0
                    y_collision = True
                else:
                    y_collision = False
                #if the com=bined x and y change would cause an overlap, set both to 0
                if (collision_mask.overlap(player_mask, (player.rect.x + move[0], player.rect.y + move[1]))):
                    move[0] = 0
                    move[1] = 0
                    #x_collision = True
                    #y_collision = True
                if (x_collision == True) or (y_collision == True):
                    if active_collision == False:
                        thud.play()
                        active_collision = True
                else:
                    active_collision = False

                for c in coins:
                    if (c.mask.overlap(player_mask, (player.rect.x - c.rect.x, player.rect.y - c.rect.y))):
                        pygame.mixer.Sound("Assets/Sounds/explosion.wav").play()
                        coins.remove(c)
                        player.inventory.coin_count += 1
                        all_sprites.remove(c)
                

            else:
                active_collision = False
            #x_collision = False
            #y_collision = False
            #send the cleaned movement coords to player.update
            player.update(move)
            camera.update(player)
            ui.update()

            # Draw calls for objects (aka: rendering)

            # Drawing the background
            screen.blit(background_image, camera.apply(background_rect))

            #comment this line out to make collision map invisible
        #    screen.blit(collision, camera.apply(background_rect))


            # Drawing all objects that we added to all_sprites
            for sprite in all_sprites:
                screen.blit(sprite.image, camera.apply(sprite))

            # Drawing the foreground
            screen.blit(foreground_image, camera.apply(foreground_rect))

            #for c in coins:
            #    screen.blit(c.mask_image, camera.apply(c.rect))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Drawing the UI
            #screen.blit(ui.drawUI(), ((screen_width - ui.drawUI().get_width()) // 2, (screen_height - ui.drawUI().get_height()) // 2))
            ui.drawUI(screen, screen_width, screen_height, font, heart, heart_rect)
            #screen.blit(text_surface, ((screen_width - text_surface.get_width()) // 2, (screen_height - text_surface.get_height()) // 2))

            # Refresh (or else the old stuff stays)
            pygame.display.flip()

            # Cap frame rate
            clock.tick(frame_rate)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


def options():
    pygame.display.set_caption("Options")

    while True:

        mouse_pos = pygame.mouse.get_pos()
        screen.fill("black")

        options_text = menu_button_font.render("Options", True, "White")
        options_rect = options_text.get_rect(center=(385, 100))
        screen.blit(options_text, options_rect)

        button_options = Button(250, 450, white_blank_menu, "Back", menu_button_font)

        if button_options.is_clicked(mouse_pos):
            button_options.image = red_blank_menu
        elif not button_options.is_clicked(mouse_pos):
            button_options.image = white_blank_menu
        button_options.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_options.is_clicked(mouse_pos):
                    main_menu()
        pygame.display.update()

def main_menu():
    # Starting the game loop
    clock = pygame.time.Clock()
    running = True

    while running:

        # Mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        # Drawing the background
        screen.blit(BG, BG.get_rect())

        for button in menu_buttons:
            if button.is_clicked(mouse_pos):
                button.image = red_blank_menu
            elif not button.is_clicked(mouse_pos):
                button.image = white_blank_menu
            button.draw(screen)

        # Update calls for objects (aka: ticking)


        # Draw calls for objects (aka: rendering)

        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_pos):
                    play()
                if options_button.is_clicked(mouse_pos):
                    options()
                if quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()

        # Cap frame rate
        clock.tick(frame_rate)


    # Quit
    pygame.quit()
    sys.exit()

main_menu()