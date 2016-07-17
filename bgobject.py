import pygame, constants, sys, json
from pygame.locals import *
from sprite import SpriteSheet

class BgObj(pygame.sprite.Sprite):

    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        self._change_x = 0
        self._change_y = 0
        self._right_catch = pygame.Rect(constants.DWIDTH+50, -10, 50, constants.DHEIGHT+20)
        self._left_catch = pygame.Rect(-60, -10, 50, constants.DHEIGHT+20)

    def set_speed(self, speed_x, speed_y):
        self._change_x = speed_x
        self._change_y = speed_y
        
    def update(self):
        self.rect.x += self._change_x
        self.rect.y += self._change_y
        if self._right_catch.contains(self.rect):
            self.kill()
        if self._left_catch.contains(self.rect):
            self.kill()
        return True

class BgObjects:
    _object_list = {}
    sprite_files = []
    
    def __init__(self, tileset):
        tiles= self.parse_json(tileset)
        sprite_sheet = SpriteSheet(self.sprite_files)
        self.load_tile_set(tiles, sprite_sheet)

    def load_tile_set(self, tiles, sprite_sheet):
        tile_map = {}
        for tile in tiles:
            tile_image = sprite_sheet.get_image(int(tile['x']),
                                                int(tile['y']),
                                                int(tile['w']),
                                                int(tile['h']),
                                                self.bgcolor, 47, 47)
            title = tile['name']
            obj = BgObj(tile_image)
            tile_map[title] = obj
        self._object_list = tile_map

    def get_object_list(self):
        #Returns the list of objects loaded
        return self._object_list.keys()
        
    def get_object(self, key):
        if key in self._object_list:
            return self._object_list[key]
        else:
            return False

    def parse_json(self, build_json):
        file_json = []
        with open(build_json) as data_file:
            data = json.load(data_file)
            for file in data['file']:
                self.sprite_files.append(file)
            self.bgcolor = (int(data['bgcolor']['red']),
                            int(data['bgcolor']['green']),
                            int(data['bgcolor']['blue']))
            for sprite in data['sprites']:
                file_json.append(sprite)
            return file_json
        
##    def parse_csv(self, build_csv):
##        file_csv = []
##        with open(build_csv) as csvfile:
##            reader = csv.DictReader(csvfile)
##            for row in reader:
##                if row["type"] == "file_info":
##                    files = row["x1"].split("|")
##                    for file in files:
##                        self.sprite_files.append(file)
##                    color = row["width"].split(".")
##                    self.bgcolor = (int(color[0]),int(color[1]),int(color[2]))
##                else:
##                    file_csv.append(row)
##        return file_csv
