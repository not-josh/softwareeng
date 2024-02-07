import pygame, sys
from Button import Button 
from UI import UI
from Player import Player
from Camera import Camera
import random
from Coin import Coin
from PlayerClass.Player import *
from Map import Map



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
    # Initial variables
    screen_width, screen_height = 1000, 1000
    room_width, room_height = 1000, 65536
    frame_rate = 0
    SPRITE_SCALE = 5

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

    # Starting the game loop
    clock = pygame.time.Clock()
    running = True

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
        
        # Update calls for objects (aka: ticking)
        map.update()
        player.update()
        camera.update(player)
        ui.update()

        # Draw calls for objects (aka: rendering)
        
        screen.fill((0,0,0))

        map.render_group.render(screen, camera)
        ui.drawUI(screen, screen_width, screen_height, ui_font, heart, heart_rect)

        # Refresh (or else the old stuff stays)
        pygame.display.flip()
        
        

        f = (f + 1) % FRAMES_AVG_OVER
        # Cap frame rate
        ft = clock.tick(frame_rate)
        if (frame_rate):
            if (ft > 1 + 1000 / frame_rate): print("Single Frame: %d ms" % (ft))
        else:
            if (ft > 5): print("Single Frame: %d ms" % (ft))
        
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