

import pygame
import math

audios =  {"laser1" : "assets\sound\laser1.mp3"}
laserAudio = {"laser1" : "assets\sound\laser1.mp3"}    
def playAudio( audioname):
    pygame.mixer.music.load(audios[audioname])
    pygame.mixer.music.play(0)