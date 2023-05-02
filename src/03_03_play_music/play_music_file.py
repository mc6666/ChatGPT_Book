import pygame

# initialize pygame mixer and set up MIDI output
pygame.mixer.init()
pygame.mixer.music.load("HotelCalifornia.mid")
pygame.mixer.music.play()

# wait until MIDI playback finishes
while pygame.mixer.music.get_busy():
    continue

# cleanup
pygame.mixer.quit()