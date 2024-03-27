from Scoreboard import Scoreboard
import string
import re
import pygame

# Scoreboard.loadScores()

# print(Scoreboard.toStr())

# Scoreboard.export()

pygame.init()

FILLCOL = (20,20,20)
screen = pygame.display.set_mode((800, 720))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 40)
sb = Scoreboard((500,500), (255,255,255), font)
sb.span = ((100,100), (600,600))

running = True
while running:
	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	screen.fill(FILLCOL)

	screen.blit(sb.surface, sb.rect.topleft)

	pygame.display.flip()
	clock.tick(60)