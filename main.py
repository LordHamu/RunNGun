"""
Basic Shooter
Author: Clayton Headley
Description: I'm trying to create a basic LARPG setup using my understanding
gained from gaming over many years.
"""

import os, sys
import pygame
import constants
from pygame.locals import *
from game import Game

class GameMain:
    """
    Main - This is the core class that creates and initializes the game
    """
    mainClock = pygame.time.Clock()
    
    def __init__(self):
        self._running = True
        self._display_surface = None
        self.size = self.width, self.height = constants.DWIDTH, constants.DHEIGHT

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, 0, 32)
        pygame.display.set_caption('Basic Run & Gun')
        self._running = True
        self._game = Game()
        
    def on_loop(self):
        self._game.update()

    def on_render(self):
        self._display_surface.fill(constants.BLACK)
        self._display_surface = self._game.draw(self._display_surface)
        pygame.display.update()
        self.mainClock.tick(30)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        try:
            if self.on_init() == False:
                self._running = False
        except:
            self.on_cleanup()
            raise
 
        while( self._running ):
            try:
                for event in pygame.event.get():
                    self._game.on_event(event)
                self.on_loop()
                self.on_render()
            except:
                self.on_cleanup()
                raise
        self.on_cleanup()

if __name__ == "__main__" :
    Client = GameMain()
    Client.on_execute()
