import pygame
from pygame.locals import *
from Button import Button

# Initialize Pygame
pygame.init()

# Colors
white = (255,255,255)
black = (0,0,0)

# Set up the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Lightning Bolt Town')
clock = pygame.time.Clock()

# Button setup
menu_button_font = pygame.font.Font(None, 48)
img_button_hover = pygame.image.load("assets/sprites/menu/Button_Hover.png")
img_button = pygame.image.load("assets/sprites/menu/Button.png")
# Scaling button assets
button_scale = .33
img_button_hover = pygame.transform.scale(img_button_hover, (int(img_button_hover.get_width() * button_scale), int(img_button_hover.get_height() * button_scale)))
img_button = pygame.transform.scale(img_button, (int(img_button.get_width() * button_scale), int(img_button.get_height() * button_scale)))

# Logo
logo_scale = .50
img_logo = pygame.image.load("assets/sprites/menu/logo.png")
img_logo = pygame.transform.scale(img_logo, (int(img_logo.get_width() * logo_scale), int(img_logo.get_height() * logo_scale)))
# Logo Text
logo_font = pygame.font.Font(None, 65)
textsurface_logo = logo_font.render("Lightning Bolt Town", True, (255, 255, 255))


# Buttons
play_button = Button(275, 300, img_button, "Play", menu_button_font)
options_button = Button(50, 475, img_button, "Options", menu_button_font)
quit_button = Button(505, 475, img_button, "Quit", menu_button_font)

buttons = [play_button, options_button, quit_button]

# Main game loop
while True:

    # Getting mouse data
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    # Rendering
    screen.fill(black)

    # Logo
    screen.blit(img_logo, (315, 25))
    screen.blit(textsurface_logo, (275 + ((240 - textsurface_logo.get_width()) // 2), 50 + 27))

    # Check for hover
    for button in buttons:
        button.draw(screen, mouse_pos)

    # Check for clicking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Cycle through the buttons that can be clicked -> perform their action
            if play_button.is_clicked(mouse_pos):
                print("Play")
            if options_button.is_clicked(mouse_pos):
                print("Options")
            if quit_button.is_clicked(mouse_pos):
                print("Quit")
            

    pygame.display.flip()
    clock.tick(60)
