import pygame, constants, sys
from pygame.locals import *
from pawn import Pawn

class Player(Pawn):
    
    def __init__(self, build_json):
        self.direction = 'R'
        self._player_max_hp = 100
        self._player_hp = 100
        self._invuln_timer = 300
        self._shooting_timer = 30
        self.cycle_frame = 0
        self.climb_frame = 0
        self._falling = True
        self._shooting = False
        self._climbing = False
        self._invuln = False
        self._blink = True    
        Pawn.__init__(self, build_json)
        self.rect = pygame.Rect((self.char_x/3, self.char_y/4),
                                ((self.char_x*2/3), self.char_y))
    
    def update(self, monsters, platform, ladder):
        hits_list = pygame.sprite.spritecollide(self, monsters, False)
        for hit in hits_list:
            if self._invuln:
                break;
            else:
                damage = hit.deal_damage()
                self.take_damage(int(damage))
                self._invuln = True

        if self._invuln:
            self._invuln_timer -= 1
        if self._invuln_timer < 0:
            self._invuln = False
            self._blink = True
            self._invuln_timer = 300
        if not(self._climbing):
            self._change_y += 2
            if self._change_y > 30: self._change_y = 30
        self.rect.x += self._change_x
        self.colide(self._change_x, 0, platform)
        self.rect.y += self._change_y
        self.colide(0, self._change_y, platform)

    def draw(self):
        if self._falling:
            if self._shooting:
                image = self.sprite_list['fallshoot'].copy()
            else:
                image = self.sprite_list['fall'].copy()
        elif self._shooting and not(self.walk):
            if self._climbing:
                image = self.sprite_list['climbshoot'].copy()
            else:
                image = self.sprite_list['shoot'].copy()
        elif self._climbing:
                cycle = self.cycle['climb']
                if self.climb_frame > 1:
                    self.climb_frame = 0
                image = self.sprite_list[cycle[self.climb_frame]].copy()
        else:
            # Figure out cycle to use:   
            if self.walk:
                cycle = self.cycle['walk']
                if self._shooting:
                    cycle = self.cycle['walk&shoot']
            else:
                cycle = self.cycle['blink']

            cycleNum = int(self.cycle_frame / 5)
            if cycleNum >= (len(cycle)-1):
                self.cycle_frame = 0
                cycleNum = 0
            frame = cycle[cycleNum]
            image = self.sprite_list[frame].copy()
            self.cycle_frame = self.cycle_frame + 1
            
        if self._invuln:
            if self._blink:
                self._blink = False
            else:
                image.set_alpha(100)
                self._blink = True
        if self.direction == "L":
            image = pygame.transform.flip(image, True, False)

        return image

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.direction = "L"
        if not(self._climbing):
            self.walk = True
            self._change_x = -12

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.direction = "R"
        if not(self._climbing):
            self._change_x = 12
            self.walk = True

    def jump(self):
        self._climbing = False
        if not self._falling:
            self._change_y = -30
            self._falling = True
        self.cycle_frame = 0

    def go_up(self, ladders):
        if self.ladder_check(ladders):
            self._climbing = True
            self._falling = False
            self._change_y = -10
            self.climb_frame += 1
        else:
            self._climbing = False
            
    def go_down(self, ladders):
        if self.ladder_check(ladders):
            self._climbing = True
            self._falling = False
            self._change_y = 10
            self.climb_frame += 1
        else:
            self._climbing = False

    def stop(self, ladders):
        """ Called when the user lets off the keyboard. """
        self.walk = False
        self.cycle_frame = 0
        self._change_x = 0
        if self._climbing and self.ladder_check(ladders):
            self._change_y = 0
        else:
            self._change_y = 12
            self._falling = True
        self._shooting = False

    def ladder_check(self, ladders):
        for ladder in ladders:
            if pygame.sprite.collide_rect(self, ladder):
                return True
        return False
                    
    def shoot(self):
        self._shooting = True
        if self._falling or self._climbing:
            return [self.direction, self.rect.x, self.rect.y - 10]
        else:
            return [self.direction, self.rect.x, self.rect.y]

    def stop_shoot(self):
        self._shooting = False
        return True

    def colide(self, x, y, platform_list):
        if not(self._climbing):
            self._falling = True
        for platform in platform_list:
            if pygame.sprite.collide_rect(self, platform):
                #print(self.rect, platform.rect)
                if x > 0:
                    self.rect.right = platform.rect.left - 1
                if x < 0 :
                    self.rect.left = platform.rect.right + 1
                if y > 0:
                    self.rect.bottom = platform.rect.top - 1
                    self._falling = False
                    self._change_y = 0
                elif y < 0:
                    self.rect.top = platform.rect.bottom + 1
                    self._change_y = 0

    def get_life(self):
        return self._player_hp

    def take_damage(self, dam):
        self._player_hp = self._player_hp - dam
        if self._player_hp < 0:
            self._player_hp = 0
        return self.player_death()

    def heal_player(self, heal):
        self._player_hp = self._player_hp + heal
        if self._player_hp > self._player_max_hp:
            self._player_hp = self._player_max_hp
        return self.get_life()

    def player_death(self):
        if self._player_hp == 0:
            return True
        else:
            return False
        
