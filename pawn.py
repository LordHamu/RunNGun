"""
This module is used to hold the Pawn class. The Pawn represents a distructable
sprite on the screen.
"""
import pygame, json
import constants
from sprite import SpriteSheet

class Pawn(pygame.sprite.Sprite):

    def __init__(self, build_json):
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

    def update(self, sprite_list):
        return true

    def activate(self):
        return true

    def parse_json(self, build_json):
        file_json = []
        with open(build_json) as data_file:
            data = json.load(data_file)
            if data['type'] == "Animated":
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

##    def parse_csv(self, build_csv):
##        file_csv = []
##        with open(build_csv) as csvfile:
##            reader = csv.DictReader(csvfile)
##            for row in reader:
##                if row["type"] == "T":
##                    self.animated = True
##                    files = row["x1"].split("|")
##                    for file in files:
##                        self.sprite_files.append(file)
##                    walkcycle = row["y1"].split(".")
##                    self.cycle = [int(i) for i in walkcycle]
##                    color = row["width"].split(".")
##                    self.bgcolor = (int(color[0]),int(color[1]),int(color[2]))
##                elif row["type"] == "F":
##                    files = row["x1"].split('|')
##                    for file in files:
##                        self.sprite_files.append(file)
##                else:
##                    file_csv.append(row)
##        return file_csv

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
        return sprite_list

##    def build_cycle(self, sprite_sheet, csv):
##
##        #Walkcycle
##        self.cycle_frame = 0
##        self.animated = True
##
##        # This holds all the images for the animated walk left/right
##        # of our player
##        self.walking_frames_l = []
##        self.walking_frames_r = []
##        self.walking_frames_u = []
##        self.walking_frames_d = []
##        self.animation = []
##        for line in csv:
##            image = sprite_sheet.get_image(int(line["x1"]), int(line["y1"]), int(line["width"]), int(line["height"]), self.bgcolor)
##            if line['type'] == 'S':
##                self.walking_frames_r.append(image)
##                image = pygame.transform.flip(image, True, False)
##                self.walking_frames_l.append(image)
##            else:
##                if line["type"] == 'U':
##                    self.walking_frames_u.append(image)
##                elif line["type"] == 'D':
##                    self.walking_frames_d.append(image)
##                elif line["type"] == 'R':
##                    self.static_image = sprite_sheet.get_image(int(line["x1"]), int(line["y1"]), int(line["width"]), int(line["height"]), self.bgcolor)
##                else:
##                    self.animation.append(image)
        
