import pygame, constants, sys
from pygame.locals import *

class Text:

    def text_objects(text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()
