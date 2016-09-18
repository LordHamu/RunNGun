import pygame, constants, sys
from pygame.locals import *

class Lifebar:
    _total_life = 0
    _current_life = 0
    _bar_width = 0

    def __init__(self, x, y, width, height, adj=False):
        self._bar_width = width
        self._bar_height = height
        self._bar_adjust = adj
        self._x = x
        self._y = y
        self._red_bar = (0,0,self._bar_width, self._bar_height)
        self._green_bar = (0,0,self._bar_width, self._bar_height)

    def draw(self, image):
        #draw the bar
        hpbar = pygame.Surface([self._bar_width + 15, self._bar_height + 15]).convert()
        hpbar.fill((200,200,200))
        pygame.draw.rect(hpbar, constants.RED, [5,
                                                5,
                                                self._red_bar[2]+5,
                                                self._red_bar[3]+5])
        pygame.draw.rect(hpbar, constants.GREEN, [5,
                                                  5,
                                                  self._green_bar[2]+5,
                                                  self._green_bar[3]+5])
        image.blit(hpbar, [self._x, self._y])
        return image

    def update(self, player):
        self.adjust_hp(player.get_life())

    def set_hp(self, hp):
        self._total_life = hp
        self._current_life = hp

    def adjust_hp(self, hp):
        self._current_life = hp
        percent = self._current_life / self._total_life
        if percent > 1:
            percent = 1
        if self._bar_adjust:
            adj = self._bar_height * percent
            self._green_bar = (0, self._bar_height - adj, self._bar_width, adj+1)
        else:
            adj = self._bar_width * percent
            self._green_bar = (self._bar_width - adj, 0, adj+1, self._bar_height)
        
        
        
