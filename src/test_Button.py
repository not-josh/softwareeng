import pygame
from pygame.locals import *
from Button import Button

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Buttons!')
clock = pygame.time.Clock()

# Button setup
menu_button_font = pygame.font.Font(None, 48)
img_button_hover = pygame.image.load("assets/sprites/menu/Button_Hover.png")
img_button = pygame.image.load("assets/sprites/menu/Button.png")
# Scaling button assets
button_scale = .33
img_button_hover = pygame.transform.scale(img_button_hover, (int(img_button_hover.get_width() * button_scale), int(img_button_hover.get_height() * button_scale)))
img_button = pygame.transform.scale(img_button, (int(img_button.get_width() * button_scale), int(img_button.get_height() * button_scale)))

play_button = Button(250, 300, img_button, "Play", menu_button_font)

# Main game loop
while True:

    # Getting mouse data
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()


    # Draw everything
    screen.fill((0, 0, 0))  # White background

    # Check for hover
    if play_button.is_clicked(mouse_pos):
        play_button.image = img_button_hover
    elif not play_button.is_clicked(mouse_pos):
        play_button.image = img_button
    play_button.draw(screen)

    # Check for clicking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_clicked(mouse_pos):
                print("Button was clicked")

    #screen.blit(sprite.image, camera.apply(sprite.rect.topleft))

    pygame.display.flip()
    clock.tick(60)
