"""
Basic Shooter
Author: Clayton Headley
Description: I'm trying to create a basic shooter setup using my understanding
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
        self.tick = 30
        self.size = self.width, self.height = constants.DWIDTH, constants.DHEIGHT

    def on_init(self):
        pygame.init()
        pygame.key.set_repeat(self.tick * 5,self.tick * 5)
        self._display_surface = pygame.display.set_mode(self.size, 0, 32)
        pygame.display.set_caption('Basic Run & Gun')
        self._running = True
        self._game = Game()
        
    def on_loop(self):
        self._game.update()

    def on_render(self):
        self._display_surface.fill(self._game.backdrop)
        self._display_surface = self._game.draw(self._display_surface)
        pygame.display.update()
        self.mainClock.tick(self.tick)

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

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
