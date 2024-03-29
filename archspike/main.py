import pygame, sys
from Button import Button 
from UI import UI
from Player import Player
from Camera import Camera
import random
from Coin import Coin
#from PlayerClass.Player import *
from Map import Map
import Collision
import LightningBolt

# Initial variables
screen_width, screen_height = 1000, 1000
room_width, room_height = 1000, 65536
frame_rate = 60
SPRITE_SCALE = 5

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")
menu_button_font = pygame.font.Font(None, 56)

# Getting assets
BG = pygame.image.load("Assets/Background/TitleScreen_bgd.png")
music_titlescreen = pygame.mixer.music.load("Assets/Music/TitleScreen.mp3")
pygame.mixer.music.set_volume(0.25)

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

    FRAMES_AVG_OVER = 300 if frame_rate == 0 else frame_rate

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Room Gen / Rendering")

    # Making an instance of the Player and placing them in the center of the screen
    player = Player("Assets/doux.png", (24, 24), 24, 0, 0, SPRITE_SCALE)

    # Making a camera that is the size of the room
    camera = Camera(room_width, room_height, screen_width, screen_height)

    # Creating the UI and its dependencies
    ui = UI(50, 50, 0)
    ui_font = pygame.font.Font(None, 36)
    heart = pygame.image.load("Assets/heart.png")
    heart_rect = heart.get_rect()

    # Create map
    map = Map(player)
    map.fillRenderGroup()
    collision = pygame.mask.Mask((room_width, map.rh*3))
    #roof_collision = pygame.mask.Mask((room_width, room_below.rect.bottom-room_above.rect.top))
    roof_collision = pygame.mask.Mask((room_width, map.rh*3))
    chng = 1

    player_last_room = -1

    # Starting the game loop
    clock = pygame.time.Clock()
    running = True
    bolt_exists = False
    bolt_move = False

    f = 0
    ft = 0
    tft = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("Player is in room %d" % (map.getPlayerRoom()), map.player.rect.center)

        # Spawn a lightning bolt
        if (pygame.key.get_pressed()[pygame.K_l]):
            bolt_exists = True
            bolt_move = True
            lightning_bolt = LightningBolt.LightningBolt("Assets/Enemies", (24,24), 0, 500, player.rect.top-500, 2)
        
        # Get player lovation and movement attempts
        player_room_index = map.getPlayerRoom() + map.render_start
        player_move = player.get_pos_change()
        if (bolt_move): l_move = lightning_bolt.get_pos_change(player.rect.center)
        
        for room_index in range(player_room_index-1, player_room_index+2):
            if (0 <= room_index < len(map.room_list)):
                room = map.room_list[room_index]
                
                # Player collisions
                player_offset = (player.rect.left-room.rect.left, player.rect.top-room.rect.top)
                player_move = Collision.collision_stop(room.mask, player.mask, player_offset, player_move)

                # Lightning collisions
                if (bolt_move):
                    l_offset = (lightning_bolt.rect.left-room.rect.left, lightning_bolt.rect.top-room.rect.top)
                    l_move = Collision.collision_stop(room.roof_mask, lightning_bolt.mask, l_offset, l_move)

        # Move player
        player.move(player_move)
        # Move lightning
        health_dec = 0
        if (bolt_move):
            lightning_bolt.update(l_move)
            if (lightning_bolt.time == 0):
                if player.rect.collidepoint((lightning_bolt.rect.center)):
                    health_dec = 10
                lightning_bolt.strike()
                bolt_move == False
                
            
        
        # Update calls for objects (aka: ticking)
        prev_score = player.inventory.coin_count 
        map.checkInteractions()
        score_diff = player.inventory.coin_count - prev_score
        chng = map.update()
        camera.update(player)
        ui.update()
        ui.loot += score_diff
        ui.current_hp -= health_dec
        
        # Shift lightning if map is shifted
        if (chng and bolt_exists):
            # Player moved up (-), all shifted down (+)
            if (chng == 1):
                lightning_bolt.move((0, map.rh))
            # Player moved down (+), all shifted up (-)
            if (chng == -1):
                lightning_bolt.move((0, -map.rh))

        # Draw calls for objects (aka: rendering)
        screen.fill((0,0,0))
        map.render_group.render(screen, camera)

        if (pygame.key.get_pressed()[pygame.K_m]):
            screen.blit(map.room_list[player_room_index].mask.to_surface(), camera.apply(map.room_list[player_room_index].rect.topleft))
            screen.blit(player.mask.to_surface(), camera.apply(player.rect.topleft))

        if (pygame.key.get_pressed()[pygame.K_n]):
            screen.blit(map.room_list[player_room_index].roof_mask.to_surface(), camera.apply(map.room_list[player_room_index].rect.topleft))

        if (bolt_exists == True):
            screen.blit(lightning_bolt.image, camera.apply(lightning_bolt.rect.topleft))
        


        ui.drawUI(screen, screen_width, screen_height, ui_font, heart, heart_rect)

        # Refresh (or else the old stuff stays)
        pygame.display.flip()

        f = (f + 1) % FRAMES_AVG_OVER
        # Cap frame rate
        ft = clock.tick(frame_rate)
        if (frame_rate):
            if (ft > 1 + 1000 / frame_rate): pass#print("Single Frame: %d ms" % (ft))
        else:
            if (ft > 5): pass# print("Single Frame: %d ms" % (ft))

        tft += ft
        if not f:
            if (frame_rate):
                print("%3.2f / %3.2f (ms/frame)" % (tft / FRAMES_AVG_OVER, 1000 / frame_rate))
            else:
                print("%3.2f (ms/frame)" % (tft / FRAMES_AVG_OVER))
            tft = 0

    # Quit
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