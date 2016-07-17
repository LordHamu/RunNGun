import pygame, constants, sys
from pygame.locals import *
from pawn import Pawn

class Monster(Pawn):

    def __init__(self, build_json, move_cycle, track_size):
        self._monster_hp = 100
        self._monster_damage = 10
        self._monster_track = 0
        self._monster_direction = "L"
        self._monster_cycle = move_cycle
        self._track_size = track_size
        Pawn.__init__(self, build_json)
        self._right_catch = pygame.Rect(constants.DWIDTH+50, -10, 50, constants.DHEIGHT+20)
        self._left_catch = pygame.Rect(-100, -10, 50, constants.DHEIGHT+20)
        
    def update(self, sprite_list):
        self.ai()
        self.rect.x += self._change_x
        self.rect.y += self._change_y
        if self._right_catch.contains(self.rect):
            self.kill()
        if self._left_catch.contains(self.rect):
            self.kill()
        self.image = self.sprite_list['center'].copy()
        
    def ai(self):
        if self._monster_track == self._track_size:
            self.mon_dir = self._monster_direction
            self._monster_direction = self._monster_cycle.pop(0)
            self._monster_cycle.append(self.mon_dir)
            self._monster_track = 0
            self._change_x = 0
            self._change_y = 0
        move = {"D": self.go_down,
                "U": self.go_up,
                "L": self.go_left,
                "R": self.go_right}
        move[self._monster_direction]()
        

    def go_left(self):
        self._change_x = -6
        self._monster_track += 1
        self.walk = True

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self._change_x = 6
        self._monster_track += 1
        self.walk = True

    def go_up(self):
        self._change_y = -12
        self._monster_track += 1
        self.walk = True

    def go_down(self):
        self._change_y = 12
        self._monster_track += 1
        self.walk = True

    def take_damage(self, dam):
        self._monster_hp = self._monster_hp - dam
        if self._monster_hp < 0 :
            self._monster_hp = 0
        return self.monster_death()

    def deal_damage(self):
        return self._monster_damage
    
    def monster_death(self):
        if self._monster_hp == 0:
            self.kill()
            return True
        else:
            return False
