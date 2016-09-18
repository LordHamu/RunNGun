import pygame, json
from pygame import *
from sprite import SpriteSheet

class Platform(pygame.sprite.Sprite):
    def __init__(self, tile, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((47*width, 47*height)).convert()
        self.image.fill((240,123,255))
        self.image.set_colorkey((240,123,255))
        for y in range(height):
            for x in range(width):
                self.image.blit(tile, (x*47, y*47))
        self.rect = self.image.get_rect()
        
class Scenery(pygame.sprite.Sprite):
    def __init__(self, tile, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((width, height)).convert()
        self.image.fill((240,123,255))
        self.image.set_colorkey((240,123,255))
        self.image.blit(tile, (0, 0))
        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, level):
        import constants
        pygame.sprite.Sprite.__init__(self)
        image = pygame.Surface([15, 10]).convert()
        pygame.draw.ellipse(image, constants.WHITE,((0,0),(15,10)))
        self.image = image
        self.rect = image.get_rect()
        self._change_x = 0
        self._change_y = 0
        self._right_catch = pygame.Rect(level.width+50, -10, 50, level.height+20)
        self._left_catch = pygame.Rect(-60, -10, 50, level.height+20)

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
        
class Level:
    def __init__(self, level):
        self._object_list = {}
        self.sprite_files = []
        self.platforms = []
        self.ladders = []
        self.blocksize = 47
        tiles = self.parse_level_json(level)
        sprite_sheet = SpriteSheet(self.sprite_files)
        self.load_tile_set(tiles, sprite_sheet)
        self.rect = Rect(0,0,self.width, self.height)

    def load_tile_set(self, tiles, sprite_sheet):
        tile_map = {}
        for tile in tiles:
            tile_image = sprite_sheet.get_image(int(tile['x']),
                                                int(tile['y']),
                                                int(tile['w']),
                                                int(tile['h']),
                                                self.bgcolor,
                                                self.blocksize,
                                                self.blocksize)
            title = tile['name']
            tile_map[title] = tile_image
        self._object_list = tile_map

    def parse_level_json(self, data):
        file_json = []
        for file in data['file']:
            self.sprite_files.append(file)
        self.bgcolor = (int(data['bgcolor']['red']),
                        int(data['bgcolor']['green']),
                        int(data['bgcolor']['blue']))
        for sprite in data['sprites']:
            file_json.append(sprite)
        for platform in data['platforms']:
            self.platforms.append(platform)
        for ladder in data['ladders']:
            self.ladders.append(ladder)
        for scenery in data['scenery']:
            self.scenery.append(scenery)
        self.width = int(data['dimensions']['width']) * self.blocksize
        self.height = int(data['dimensions']['height']) * self.blocksize
        self.player_x = int(data['player_start']['x']) * self.blocksize
        self.player_y = int(data['player_start']['y']) * self.blocksize
        self.backdrop = (int(data['background_fill']['red']),
                        int(data['background_fill']['green']),
                        int(data['background_fill']['blue']))
        return file_json
        
    def build_platforms(self):
        p_list = []
        for p in self.platforms:
            platform = Platform(self._object_list[p['tile']],
                                p['w'],
                                p['h'])
            platform.rect.x = int(p['x'])* self.blocksize
            platform.rect.y = int(p['y'])* self.blocksize
            p_list.append(platform)
        return p_list
        
    def build_ladders(self):
        l_list = []
        for l in self.ladders:
            ladder = Platform(self._object_list[l['tile']],
                                l['w'],
                                l['h'])
            ladder.rect.x = int(l['x'])* self.blocksize
            ladder.rect.y = int(l['y'])* self.blocksize
            l_list.append(ladder)
        return l_list
