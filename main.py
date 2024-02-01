import pygame, sys
from Button import Button 

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")
menu_button_font = pygame.font.Font(None, 56)

BG = pygame.image.load("Assets/Background/TitleScreen_bgd.png")
frame_rate = 60

white_blank_menu = pygame.image.load("Assets/Menu/White_Blank.png")
red_blank_menu = pygame.image.load("Assets/Menu/Red_Blank.png")

white_blank_menu = pygame.transform.scale(white_blank_menu, (int(white_blank_menu.get_width() * 2.5), int(white_blank_menu.get_height() * 2.5)))
red_blank_menu = pygame.transform.scale(red_blank_menu, (int(red_blank_menu.get_width() * 2.5), int(red_blank_menu.get_height() * 2.5)))

play_button = Button(250, 300, white_blank_menu, "Play", menu_button_font)
options_button = Button(250, play_button.y + 150, white_blank_menu, "Options", menu_button_font)
quit_button = Button(250, options_button.y + 150, white_blank_menu, "Quit", menu_button_font)

menu_buttons = [play_button, options_button, quit_button]

def get_font(size):
    pass

def play():
    pass

def options():
    pass

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
            if button.is_clicked(mouse_pos) and mouse_buttons[0] == 1:
                print("clicked")
            button.draw(screen)

        # Update calls for objects (aka: ticking)


        # Draw calls for objects (aka: rendering)

        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()

        # Cap frame rate
        clock.tick(frame_rate)


    # Quit
    pygame.quit()
    sys.exit()

main_menu()