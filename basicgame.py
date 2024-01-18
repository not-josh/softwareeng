# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("ligHTning Bolt TOWN!!!")
clock = pygame.time.Clock()
running = True
dt = 0
timer = 120

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
#Makes a COPY of the player's current position vector to use for lightning pos.
#If i used an = to copy it, then i would just be using the address, which would continue to update (not what i want)
lightning_pos = player_pos.copy()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    #screen.fill("darkslategrey")
    screen.fill("midnightblue")

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    if (timer == 60):   #if one second has passed/one second remains
         lightning_pos = player_pos.copy()  #copy the players pos
    if (timer <= 60) and (timer > 30):      #constantly draw a grey circle "target" at the spot where lightning will strike
        pygame.draw.circle(screen, "grey27", lightning_pos, 40)
    if (timer <= 30) and (timer > 0):       #for the final half second
        pygame.draw.circle(screen, "yellow", lightning_pos, 40) #draw a yellow circle (the lightning bolt)
    if (timer == 0):
        timer = 120 #sets timer to 2 seconds
    timer -= 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()