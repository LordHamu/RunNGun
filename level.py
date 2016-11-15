import pygame, json
from pygame import *
from sprite import SpriteSheet
from spawner import Spawner
from monster import Monster

class Platform(pygame.sprite.Sprite):
    def __init__(self, tile, width, height, cx = 0, cy = 0):
        pygame.sprite.Sprite.__init__(self)
        self.cx = cx
        self.cy = cy
        self.image = Surface((width*50, height*50)).convert()
        self.image.fill((240,123,255))
        self.image.set_colorkey((240,123,255))
        for y in range(height):
            for x in range(width):
                self.image.blit(tile, (x*50, y*50))
        self.rect = self.image.get_rect()

    def update(self, sprite_list):
        self.rect.x += self.cx
        self.rect.y += self.cy
        
class Door(pygame.sprite.Sprite):
    def __init__(self, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((50, 50*4)).convert()
        self.image.fill((240,123,255))
        self.image.set_colorkey((240,123,255))
        for y in range(4):
            for x in range(1):
                self.image.blit(tile, (x*50, y*50))
        self.rect = self.image.get_rect()
        self.level = ''
        self.px = 0
        self.py = 0
        self.dir = "R"
        
class Scenery(pygame.sprite.Sprite):
    def __init__(self, tile, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((width, height)).convert()
        self.image.fill((240,123,255))
        self.image.set_colorkey((240,123,255))
        self.image.blit(tile, (0, 0))
        self.rect = self.image.get_rect()

class Teleport(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((100, 150)).convert()
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.width = 25
        self.rect.x = x*50+25
        self.rect.y = y*50

    def warp(self, players):
        hit_list = pygame.sprite.spritecollide(self, players, False)
        if len(hit_list)>0:
            return True
        else:
            return False
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, level, damage):
        import constants
        pygame.sprite.Sprite.__init__(self)
        image = pygame.Surface([15, 10]).convert()
        pygame.draw.ellipse(image, constants.WHITE,((0,0),(15,10)))
        self.image = image
        self.damage = damage
        self.rect = image.get_rect()
        self._change_x = 0
        self._change_y = 0
        self._right_catch = pygame.Rect(level.width+50, -10, 50, level.height+20)
        self._left_catch = pygame.Rect(-60, -10, 50, level.height+20)

    def set_speed(self, speed_x, speed_y):
        self._change_x = speed_x
        self._change_y = speed_y
        
    def update(self, platform):
        hits_list = pygame.sprite.spritecollide(self, platform, False)
        for hit in hits_list:
            self.kill()
        self.rect.x += self._change_x
        self.rect.y += self._change_y
        if self._right_catch.contains(self.rect):
            self.kill()
        if self._left_catch.contains(self.rect):
            self.kill()

    def deal_damage(self):
        return self.damage
    
        
class Level:
    def __init__(self, level):
        self._object_list = {}
        self.sprite_files = []
        self.platforms = []
        self.ladders = []
        self.doors = []
        self.spawners = []
        self.monsters = []
        self.blocksize = 50
        self.boss = False
        self.boss_beat = False
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
                                                int(tile['w']),
                                                int(tile['h']))
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
        for door in data['doors']:
            self.doors.append(door)
        for scenery in data['scenery']:
            self.scenery.append(scenery)
        for spawner in data['spawners']:
            self.spawners.append(spawner)
        for monster in data['monsters']:
            self.monsters.append(monster)
        self.width = int(data['dimensions']['width']) * self.blocksize
        self.height = int(data['dimensions']['height']) * self.blocksize
        self.player_x = int(data['player_start']['x']) * self.blocksize
        self.player_y = int(data['player_start']['y']) * self.blocksize
        self.backdrop = (int(data['background_fill']['red']),
                        int(data['background_fill']['green']),
                        int(data['background_fill']['blue']))
        return file_json
    
    def build_mob(self, monster, location):
        if monster['flying']=='True':
            flying = True
        else:
            flying = False
        if 'shooting' in monster and monster['shooting'] == 'True':
            shooting = True
            s_speed = monster['s_speed']
        else:
            shooting = False
            s_speed = 0
        if 'hp' in monster:
            hp = monster['hp']
        else:
            hp = 100
        if 'speed' in monster:
            speed = monster['speed']
        else:
            speed = 2
        mon = Monster(monster['file'],
                      self,
                      monster['type'],
                      monster['path'],
                      flying,
                      shooting,
                      s_speed,
                      hp,
                      speed
                      )
        mon.rect.x = int(location['x'])*50
        mon.rect.y = int(location['y'])*50
        mon.type = monster['type']
        return mon

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
                                int(l['w']),
                                int(l['h']))
            ladder.rect.x = int(l['x'])* self.blocksize
            ladder.rect.y = int(l['y'])* self.blocksize
            l_list.append(ladder)
        return l_list
    
    def build_scenery(self):
        s_list = []
        for s in self.ladders:
            bgobject = Scenery(self._object_list[s['tile']],
                                int(s['w']),
                                int(s['h']))
            bgobject.rect.x = int(s['x'])* self.blocksize
            bgobject.rect.y = int(s['y'])* self.blocksize
            s_list.append(bgobject)
        return s_list

    def build_doors(self):
        d_list = []
        for d in self.doors:
            door = Door(self._object_list[d['tile']])
            door.rect.x = int(d['x'])* self.blocksize
            door.rect.y = int(d['y'])* self.blocksize
            door.level = d['level']
            door.px = d['player_x']
            door.py = d['player_y']
            door.dir = d['player_f']
            d_list.append(door)
        return d_list

    def build_spawners(self):
        s_list = []
        for spawn in self.spawners:
            spawner = Spawner(spawn)
            s_list.append(spawner)
        return s_list

    def build_monsters(self):
        m_group = pygame.sprite.Group()
        for monster in self.monsters:
            if monster['type'] == "boss":
                self.boss = True
                self.boss_mob = self.build_mob(monster, monster['location'][0])
            else:
                for location in monster['location']:
                    mon = self.build_mob(monster, location)
                    m_group.add(mon)
        return m_group

    def build_teleport(self, x, y):
        p_list = []
        teleport = [['teleport_top_left', 0, 0, 1, 1],
                    ['teleport_top_right', 1, 0, 1, 1],
                    ['teleport_bottom_left',0, 4, 1, 1],
                    ['teleport_bottom_right', 1, 4, 1, 1]]
        for p in teleport:
            platform = Platform(self._object_list[p[0]],p[3],p[4])
            platform.rect.x = (int(p[1])* self.blocksize) + ( x * self.blocksize )
            platform.rect.y = (int(p[2])* self.blocksize) + ( y * self.blocksize )
            p_list.append(platform)
        teleport = Teleport(x, y+1)
        return teleport, p_list
        
    def load_door(self, x, y):
        self.player_x = x
        self.player_y = y

    
