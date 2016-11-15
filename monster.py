import pygame, constants, sys
from pygame.locals import *
from pawn import Pawn

class Monster(Pawn):

    def __init__(self, build_json, level, m_type, move_cycle, flying, shooting,
                 s_speed, hp, speed):
        self._monster_max_hp = hp
        self._monster_hp = hp
        self._monster_damage = 10
        self._monster_track = 0
        self.cycle_frame = 0
        self.move_speed = speed
        self._falling = True
        self._flying = flying
        self._shooting = shooting
        self._shooting_speed = s_speed
        self._monster_direction = "L"
        self._type = m_type
        self._monster_cycle = move_cycle
        Pawn.__init__(self, build_json, level)
        self._right_catch = pygame.Rect(constants.DWIDTH+55, -10, 50, constants.DHEIGHT+20)
        self._left_catch = pygame.Rect(-55, -10, 50, constants.DHEIGHT+20)
        self._bottom_catch = pygame.Rect(-10, constants.DHEIGHT+10, constants.DWIDTH+20, 50) 
        
    def update(self, m_platforms, platforms, bullets, monsters, camera):
        if camera.on_camera(self):
            self._flip = True
            hits_list = pygame.sprite.spritecollide(self, bullets, False)
            for hit in hits_list:
                self.take_damage(int(hit.deal_damage()))
                hit.kill()
            bump_list = pygame.sprite.spritecollide(self, monsters, False)
            for bump in bump_list:
                if not(self == bump):
                    self._change_x = -self._change_x
                    if self._monster_direction == "R":
                        self.flip()
                        self.rect.right = bump.rect.left - self.move_speed
                    elif self._monster_direction == "L" :
                        self.flip()
                        self.rect.left = bump.rect.right + self.move_speed
            self.ai()
            if not(self._flying):
                self._change_y += 5
                if self._change_y > 30:
                    self._change_y = 30
            platform_set = pygame.sprite.Group()
            for platform in platforms:
                platform_set.add(platform)
            for m_platform in m_platforms:
                platform_set.add(m_platform)
            self.rect.x += self._change_x
            plat_list = pygame.sprite.spritecollide(self, platform_set, False)
            for plat in plat_list:
                if self._monster_direction == "R":
                    self.flip()
                    self.rect.right = plat.rect.left - self.move_speed
                elif self._monster_direction == "L" :
                    self.flip()
                    self.rect.left = plat.rect.right + self.move_speed
            self.rect.y += self._change_y
            self.colide(0, self._change_y, platform_set)
            if self._right_catch.contains(self.rect):
                self.kill()
            if self._left_catch.contains(self.rect):
                self.kill()
            if self._bottom_catch.contains(self.rect):
                self.kill()

    def draw(self):
        cycle = self.cycle['walk']
        if self._shooting:
            cycle = self.cycle['shooting']
        cycleNum = int(self.cycle_frame / 5)
        if cycleNum >= (len(cycle)-1):
            self.cycle_frame = 0
            cycleNum = 0
        frame = cycle[cycleNum]
        image = self.sprite_list[frame].copy()
        self.cycle_frame = self.cycle_frame + 1
        if self._monster_direction == "L":
            image = pygame.transform.flip(image, True, False)
        return image
        
    def ai(self):
        move = {"D": self.go_down,
                "U": self.go_up,
                "L": self.go_left,
                "R": self.go_right,
                "Jump": self.jump,
                "Shoot": self.shoot}
        move[self._monster_direction]()
        
    def flip(self):
        if self._flip :
            if self._monster_direction == "R":
                self._monster_direction = "L"
            elif self._monster_direction == "L":
                self._monster_direction = "R"
            self._flip = False
        
    def go_left(self):
        self._change_x = -self.move_speed
        self._monster_track += 1

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self._change_x = self.move_speed
        self._monster_track += 1

    def go_up(self):
        self._change_y = -12
        self._monster_track += 1

    def go_down(self):
        self._change_y = 12
        self._monster_track += 1

    def jump(self):
        if not self._falling:
            self._change_y = -60
            self._falling = True

    def shoot(self):
        self._shooting = False
        return [self.direction, self.rect.x, self.rect.y]

    def take_damage(self, dam):
        self._monster_hp = self._monster_hp - dam
        if self._monster_hp < 0 :
            self._monster_hp = 0
        return True

    def colide(self, x, y, platform_list):
        self._falling = True
        for platform in platform_list:
            if pygame.sprite.collide_rect(self, platform):
                if x > 0:
                    self.flip()
                    self._change_x = -self._change_x
                    self.rect.right = platform.rect.left - 1
                if x < 0 :
                    self.flip()
                    self._change_x = -self._change_x
                    self.rect.left = platform.rect.right + 1
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
            return True
        else:
            return False

    def get_life(self):
        return self._monster_hp

    def get_max_life(self):
        return self._monster_max_hp
