import pygame
from Player import Player
from Camera import Camera
import sys
from UI import UI
import random
from Coin import Coin
import LightningBolt

# Initial variables
screen_width, screen_height = 800, 800
camera_width, camera_height = 800, 800
room_width, room_height = 800, 800
frame_rate = 60

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
foreground_collision = pygame.mask.from_surface(foreground_image)

#Get collision mask stuff from collision map of background
collision = pygame.image.load("Assets/temptown2_collisionmap.png")
collision = pygame.transform.scale(collision, (room_width, room_height))
#collision_rect = collision.get_rect() this was in the tutorial i used but i dont think it's ever actually used
collision_mask = pygame.mask.from_surface(collision)
collision_mask_image = collision_mask.to_surface()

# Making an instance of the Player and placing them in the center of the screen
player = Player("Assets/doux.png", (24, 24), 24, screen_width // 2, screen_width // 2, SPRITE_SCALE)
player_mask = pygame.mask.from_surface(player.image)

lightning_bolt = LightningBolt.LightningBolt("Assets/Enemies", (24,24), 0, screen_width//2, screen_width//2, SPRITE_SCALE)

# Making a camera that is the size of the room
camera = Camera(room_width, room_height, screen_width, screen_height)

# Making a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(lightning_bolt)

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

    player_pos = [player.rect.x, player.rect.y]
    print(player_pos)
    l_move = lightning_bolt.get_pos_change(player_pos)
    if l_move[0] != 0 or l_move[1] !=0:
        print(l_move, lightning_bolt.rect.x, lightning_bolt.rect.y)

        #if the x change would cause an overlap, set it to 0
        if (foreground_collision.overlap(lightning_bolt.mask, (lightning_bolt.rect.x + l_move[0],lightning_bolt.rect.y + 0))):
            l_move[0] = 0
            print("collision")
        #if the y change would cause an overlap, set it to 0
        if (foreground_collision.overlap(lightning_bolt.mask, (lightning_bolt.rect.x + 0, lightning_bolt.rect.y + l_move[1]))):
            l_move[1] = 0
            print("collision")
        #if the com=bined x and y change would cause an overlap, set both to 0
        if (foreground_collision.overlap(lightning_bolt.mask, (lightning_bolt.rect.x + l_move[0], lightning_bolt.rect.y + l_move[1]))):
            l_move[0] = 0
            l_move[1] = 0
            print("collision")\
            
        lightning_bolt.update(l_move)



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


# Quit
pygame.quit()
sys.exit()