import pygame
import time

#class MusicManager:

    #def __init__(self):
music_end = None
repeat = False
current_song = None
standard_volume = 1

    # Play song
def play_song(song, repeat, volume=1):
    if current_song != song:
        current_song = song
        repeat = repeat
        set_volume(volume)
        standard_volume = volume
        pygame.mixer.music.stop()
        pygame.mixer.music.load(song)

        if repeat:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play()

    # Play sound effect
def play_soundfx(effect, volume=1):
    sound = pygame.mixer.Sound(effect)
    sound.set_volume(volume)
    sound.play()

    # Set volume
def set_volume(volume):
    pygame.mixer.music.set_volume(volume)

    # Volume check
def volume_check(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            standard_volume += .1
        elif event.key == pygame.K_DOWN:
            standard_volume -= .1
        set_volume(standard_volume)
