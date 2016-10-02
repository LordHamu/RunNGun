import pygame, constants, sys
from pygame.locals import *
from pawn import Pawn

class Monster(Pawn):

    def __init__(self, build_json, level, move_cycle, track_size, flying = False):
        self._monster_hp = 100
        self._monster_damage = 10
        self._monster_track = 0
        self._falling = True
        self._flying = flying
        self._monster_direction = "L"
        self._monster_cycle = move_cycle
        self._track_size = track_size
        Pawn.__init__(self, build_json, level)
        self._right_catch = pygame.Rect(constants.DWIDTH+55, -10, 50, constants.DHEIGHT+20)
        self._left_catch = pygame.Rect(-55, -10, 50, constants.DHEIGHT+20)
        self._bottom_catch = pygame.Rect(-10, constants.DHEIGHT+10, constants.DWIDTH+20, 50) 
        
    def update(self, m_platform, platform, bullets, monsters):
        hits_list = pygame.sprite.spritecollide(self, bullets, False)
        for hit in hits_list:
            self.take_damage(int(hit.deal_damage()))
            hit.kill()
        bump_list = pygame.sprite.spritecollide(self, monsters, False)
        for bump in bump_list:
            self.flip()
            
        self.ai()
        self.rect.x += self._change_x
        self.rect.y += self._change_y
        if not(self._flying):
            self._change_y += 5
            if self._change_y > 30:
                self._change_y = 30
        self.colide(self._change_x, 0, m_platform)
        self.colide(self._change_x, 0, platform)
        self.rect.y += self._change_y
        self.colide(0, self._change_y, m_platform)
        self.colide(0, self._change_y, platform)
        if self._right_catch.contains(self.rect):
            self.kill()
        if self._left_catch.contains(self.rect):
            self.kill()
        if self._bottom_catch.contains(self.rect):
            self.kill()
        self.image = self.sprite_list['base'].copy()

    def draw(self):
        return self.image
        
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
        
    def flip(self):
        flip_cycle = [l.replace("L", "P") for l in self._monster_cycle]
        flip_cycle = [l.replace("R", "L") for l in flip_cycle]
        flip_cycle = [l.replace("P", "R") for l in flip_cycle]
        self._monster_cycle = flip_cycle
        
    def go_left(self):
        self._change_x = -2
        self._monster_track += 1

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self._change_x = 2
        self._monster_track += 1

    def go_up(self):
        self._change_y = -12
        self._monster_track += 1

    def go_down(self):
        self._change_y = 12
        self._monster_track += 1

    def take_damage(self, dam):
        self._monster_hp = self._monster_hp - dam
        if self._monster_hp < 0 :
            self._monster_hp = 0
        return self.monster_death()

    def colide(self, x, y, platform_list):
        for platform in platform_list:
            if pygame.sprite.collide_rect(self, platform):
                if x > 0:
                    self.flip()
                    self._chnage_x = -x
                if x < 0 :
                    self.flip()
                    self._chnage_x = -x
                if not(self._flying):
                    if y > 0:
                        self.rect.bottom = platform.rect.top - 1
                        self._falling = False
                        self._change_y = 0
                    elif y < 0:
                        self.rect.top = platform.rect.bottom + 1
                        self._change_y = 0



    def deal_damage(self):
        return self._monster_damage
    
    def monster_death(self):
        if self._monster_hp == 0:
            self.kill()
            return True
        else:
            return False
