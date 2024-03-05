import pygame

class UI:
    
    # blit will handle the location

    def __init__(self, player):
        self.player = player
        self.display_text = "Hello, Pygame!"


    def draw(self, screen, font, color):
        # Draw text and UI related things here

        # Drawing health
        text_surface = font.render(self.get_hp_text(), True, color)
        screen.blit(text_surface, (29, 45))
        # Drawing score
        text_surface = font.render(self.get_score_text(), True, color)
        screen.blit(text_surface, (705, 15))

        # Draw the healthbar
        self.draw_healthbar(screen)

    
    def draw_textvalues():
        pass
    
    def draw_healthbar(self, screen):
        # Draw the full rectangle with black
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(15, 15, 100, 20))

        # Draw the current health over that bar (color varies)
        bar_color = (0, 0, 0)
        percent_health = self.player.health / self.player.max_health
        if percent_health >= .5:
            bar_color = (50, 168, 82) # Green
        elif percent_health < .5 and percent_health >= .25:
            bar_color = (226, 237, 12) # Yellow
        else:
            bar_color = (237, 12, 12) # Red
        pygame.draw.rect(screen, bar_color, pygame.Rect(17, 17, min(96 * (self.player.health / self.player.max_health) , 96), 16))


    def get_hp_text(self):
        # max_numerator used with whitespace to anchor the string so it is always centered
        max_numerator = 3
        hp_text = str(self.player.health) + " / " + str(self.player.max_health)
        whitespace = max_numerator - len((str(self.player.health)))
        hp_text = whitespace * " " + hp_text
        return hp_text
    
    def get_score_text(self):
        return "Score: " + str(self.player.points)