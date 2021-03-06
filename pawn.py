"""
This module is used to hold the Pawn class. The Pawn represents a distructable
sprite on the screen.
"""
import pygame, json
import constants
from sprite import SpriteSheet

class Pawn(pygame.sprite.Sprite):

    def __init__(self, build_json, level):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Setup the Pawn
        self.cycle = {}
        self.walk = False
        self.animated = False
        self.sprite_files = []
        self._change_x = 0
        self._change_y = 0
        self.static_image = None

        # Build the Pawn
        json = self.parse_json(build_json)
        player_layers = self.sprite_files
        sprite_sheet = SpriteSheet(player_layers)
        self.sprite_list = self.build_cycle(sprite_sheet, json)
        
        # Set a referance to the image rect.
        self.rect = self.static_image.get_rect()

        # Setup level kill zones.
        self._right_catch = pygame.Rect(level.width+55, -10, 50, level.height+20)
        self._left_catch = pygame.Rect(-55, -10, 50, level.height+20)
        self._bottom_catch = pygame.Rect(-10, level.height+10, level.width+20, 50) 

    def update(self, sprite_list):
        self.rect.x += self._change_x
        self.rect.y += self._change_y
        if self._right_catch.contains(self.rect):
            self.kill()
        if self._left_catch.contains(self.rect):
            self.kill()
        if self._bottom_catch.contains(self.rect):
            self.kill()
        return True

    def activate(self):
        return True

    def draw(self):
        return self.static_image

    def set_movement(self, x, y):
        self._change_x = x
        self._change_y = y

    def parse_json(self, build_json):
        file_json = []
        with open(build_json) as data_file:
            data = json.load(data_file)
            if data['animated'] == "True":
                self.animated = True
            for file in data['file']:
                self.sprite_files.append(file)
            self.bgcolor = (int(data['bgcolor']['red']),
                            int(data['bgcolor']['green']),
                            int(data['bgcolor']['blue']))
            self.frames = int(data['frames'])
            self.char_x = int(data['rect']['width'])
            self.char_y = int(data['rect']['height'])
            for anim in data['cycles']:
                self.cycle[anim['name']] = anim['cycle']
            for sprite in data['sprites']:
                file_json.append(sprite)
            return file_json

    def build_cycle(self, sprite_sheet, json):
        self.cycle_frame = 0
        sprite_list = {}
        for sprite in json:
            image = sprite_sheet.get_image(int(sprite["x"]),
                                           int(sprite["y"]),
                                           int(sprite["w"]),
                                           int(sprite["h"]),
                                           self.bgcolor,
                                           self.char_x,
                                           self.char_y)
            sprite_list[sprite['name']] = image
            if sprite['name'] == 'base':
                self.static_image = image
                self.image = image
        return sprite_list
