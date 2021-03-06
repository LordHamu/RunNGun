"""
Basic Shooter: Game
Author: Clayton Headley
Description: This contains all the game logic, I seperated it from the pygame
runner so that main stays uncluttered.
"""

import pygame, constants, sys, copy, json
from pygame.locals import *
from player import Player
from camera import Camera
from level import Level, Platform, Bullet
from text import Text
from menu import Menu, Game_Menu
from hpbar import Lifebar
from pawn import Pawn
from os import listdir

class Game:

    def __init__(self, debug=False):
        self._debug = debug
        self._pause = False
        self.character = "character\\megaman.json"
        self.backdrop = constants.BLACK
        self.monster_sprite_list = pygame.sprite.Group()
        self.scenery_sprite_list = pygame.sprite.Group()
        self.bullet_sprite_list = pygame.sprite.Group()
        self.player_sprite_list = pygame.sprite.Group()
        self.platform_sprite_list = pygame.sprite.Group()
        self.ladder_sprite_list = pygame.sprite.Group()
        self.door_sprite_list = pygame.sprite.Group()
        self.moving_platforms_list = pygame.sprite.Group()
        self.spawners = []
        self.ui_lifebar = []
        self.object_list = {}
        self.create_objects()
        self.ui_list = []
        self.main_menu = Menu()
        self.menu_flag = True
        self.start_level = None
        self.load_splash()

    #GAME
    def load_splash(self):
        self.clear()
        self.add_title("Run & Gun")
        self.add_button("New",(constants.DWIDTH/2)-50, 350, 100,50,
                        constants.WHITE, constants.BLUE, self.start_game)
        self.add_button("Quit",(constants.DWIDTH/2)-50, 450, 100,50,
                        constants.WHITE, constants.BLUE, self.exit_game)

    def start_game(self):
        self.clear()
        self.lives = 3
        self.ui_list += self.main_menu.draw_menu()
        self.current_level = [self.main_menu.selected_name(), 0, 0, "R"]
        
    def exit_game(self):
        pygame.quit()
        sys.exit()

    def load_level(self, level):
        if self.start_level == None:
            self.start_level = level[0]
        self.menu_flag = False
        player_hp = -1
        if hasattr(self, 'player'):
            player_hp = self.player.get_life()
        self.clear()
        self.level = Level(self.main_menu.get_level_json(level[0]))
        if level[1] != 0:
            self.level.player_x = int(level[1])
        if level[2] != 0:
            self.level.player_y = int(level[2])
        self.scenery_sprite_list = self.level.build_scenery()
        self.platform_sprite_list = self.level.build_platforms()
        self.ladder_sprite_list = self.level.build_ladders()
        self.door_sprite_list = self.level.build_doors()
        self.monster_sprite_list = self.level.build_monsters()
        self.spawners = self.level.build_spawners()
        self.backdrop = self.level.backdrop
        self.add_player(self.character, self.level.player_x,
                        self.level.player_y, level[3])
        if player_hp > 0:
            self.player.set_life(player_hp)
        self.add_camera()
        self.add_lifebar(25, 25, 'player', self.player)
        if self.level.boss and not(self.main_menu.boss_check(self.start_level)):
            self.boss = self.level.boss_mob
            self.monster_sprite_list.add(self.boss)
            self.add_lifebar(constants.DWIDTH - 50, 25, 'boss', self.boss)

    def reload_level(self):
        monsters = self.monster_sprite_list
        player_hp = self.player.get_life()
        self.menu_flag = False
        self.clear()
        self.monster_sprite_list = monsters
        self.scenery_sprite_list = self.level.build_scenery()
        self.platform_sprite_list = self.level.build_platforms()
        self.ladder_sprite_list = self.level.build_ladders()
        self.door_sprite_list = self.level.build_doors()
        self.spawners = self.level.build_spawners()
        self.backdrop = self.level.backdrop
        self.add_player(self.character, self.level.player_x, self.level.player_y, "R")
        self.add_camera()
        self.player.set_life(player_hp)
        self.add_lifebar(25, 25, 'player', self.player)
        if self.level.boss and not(self.main_menu.boss_check(self.start_level)):
            self.boss = self.level.boss_mob
            self.monster_sprite_list.add(self.boss)
            self.add_lifebar(constants.DWIDTH - 50, 25, 'boss', self.boss)

    #Add functions
    def add_camera(self):
        self.camera = Camera(self.level.width, self.level.height)

    def add_lifebar(self, x, y, name, pawn):
        lifebar = Lifebar( x, y, 20, 200, True)
        lifebar.set_hp(pawn.get_max_life())
        self.ui_lifebar.append([name, lifebar])
        
    def add_title(self, title):
        TextSurf, TextRect = Text.text_objects(title, constants.largeText, constants.WHITE)
        TextRect.center = ((constants.DWIDTH / 2), ((constants.DHEIGHT / 2) - 100))
        self.ui_list.append({'title':title, 'type': 'text','surface':TextSurf,'rectangle':TextRect})

    def add_button(self, button_text, x, y, w, h, ic, ac, action=None):
        button_rect = pygame.Rect(x,y,w,h)
        button_surface = pygame.Surface((w,h))
        
        self.ui_list.append({'title':button_text, 'type':'button', 'ac':ac, 'ic':ic, 'action':action, 'rectangle':button_rect})
        textSurf, textRect = Text.text_objects(button_text, constants.smallText, constants.BLACK)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.ui_list.append({'title':button_text,'type':'button_text','surface':textSurf, 'rectangle':textRect})

    def add_bullet(self, cord):
        bullet = Bullet(self.level.rect, self.player.weapon_damage)
        if cord[0] == 'R':
            bullet.rect.x = cord[1] + 45
            bullet.rect.y = cord[2] + 40
            bullet.set_speed(18,0)
        else:
            bullet.rect.x = cord[1]+5
            bullet.rect.y = cord[2]+40
            bullet.set_speed(-18,0)
        self.bullet_sprite_list.add(bullet)
        return True

    def add_platform(self, pawn_file, cord, move):
        pawn = Pawn(pawn_file, self.level)
        pawn.rect.x = cord[0]
        pawn.rect.y = cord[1]
        pawn.set_movement(move[0], move[1])
        self.moving_platforms_list.add(pawn)
        return True
        
    def add_player(self, json, x, y, d):
        self.player = Player(json, self.level)
        rect = self.player.set_xy(x, y)
        print(rect)
        self.player.direction = d
        self.player_sprite_list.add(self.player)
    
    #Helper functions
        
    def create_objects(self):
        files = listdir("objects")
        for file in files:
            with open("objects\\"+file) as data_file:
                data = json.load(data_file)
                if data['name'] in self.object_list:
                    print("crap, names matched.")
                else:
                    self.object_list[data['name']] = "objects\\"+file

    def clear(self):
        self.backdrop = constants.BLACK
        self.monster_sprite_list = pygame.sprite.Group()
        self.scenery_sprite_list = pygame.sprite.Group()
        self.bullet_sprite_list = pygame.sprite.Group()
        self.player_sprite_list = pygame.sprite.Group()
        self.platform_sprite_list = pygame.sprite.Group()
        self.ladder_sprite_list = pygame.sprite.Group()
        self.door_sprite_list = pygame.sprite.Group()
        self.spawners = []
        self.ui_list = []
        if hasattr(self, 'camera'):
            del self.camera
        if hasattr(self, 'ui_lifebar'):
            self.ui_lifebar = []
        if hasattr(self, 'player'):
            del self.player
        if hasattr(self, 'boss'):
            del self.boss
            del self.boss_mob

    def end_level(self):
        self.main_menu.finished_level(self.start_level)
        self.start_level = None
        self.clear()
        self.menu_flag = True
        self.ui_list += self.main_menu.draw_menu()
        
    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    def character_death(self):
        if self.lives > 0:
            self.lives -= 1
            self.player.set_life(self.player.get_max_life())
            self.reload_level()
        else:
            self.clear()
            self.ui_list += self.main_menu.draw_menu()

    def change_level(self):
        change = False
        hits_list = pygame.sprite.spritecollide(self.player,
                                                self.door_sprite_list, False)
        for hit in hits_list:
            self.current_level = [hit.level, hit.px, hit.py, hit.dir]
            change = True
        return change

    def check_dead(self):
        return self.player.player_death()

    def spawn_teleport(self):
        self.teleport, plist = self.level.build_teleport(10,15)
        self.platform_sprite_list += plist
        return True

    #Pygame functions
        
    def update(self):
        if not (self._pause) and hasattr(self, 'player'):
            self.moving_platforms_list.update(self.player_sprite_list)
            self.player_sprite_list.update(self.monster_sprite_list.sprites(),
                                           self.platform_sprite_list,
                                           self.moving_platforms_list)
            self.monster_sprite_list.update(self.platform_sprite_list,
                                            self.moving_platforms_list,
                                            self.bullet_sprite_list.sprites(),
                                            self.monster_sprite_list.sprites(),
                                            self.camera)
            self.bullet_sprite_list.update(self.platform_sprite_list)
            if self.change_level():
                print("Changing level:", self.current_level)
                self.load_level(self.current_level)
            if self.check_dead():
                self.character_death()
            if hasattr(self, 'boss') and self.boss.monster_death():
                del self.boss
                self.ui_lifebar.remove(self.ui_lifebar[1])
                self.spawn_teleport()
            if hasattr(self, 'teleport'):
                if self.teleport.warp(self.player_sprite_list):
                    self.end_level()
            #Clean Up dead monsters
            for monster in self.monster_sprite_list:
                if monster.monster_death():
                    monster.kill()
            for spawner in self.spawners:
                spawn = spawner.update()
                if spawn == False:
                    pass
                elif spawn[0] == "Platform":
                    pawn_type = self.object_list[spawn[1]]
                    self.add_platform(pawn_type, spawn[2], spawn[3])
                else:
                    pass
        if hasattr(self, 'camera'):
            self.camera.update(self.player)
        if hasattr(self, 'ui_lifebar'):
            for lifebar in self.ui_lifebar:
                if lifebar[0] == "player":
                    lifebar[1].update(self.player)
                if lifebar[0] == 'boss':
                    lifebar[1].update(self.boss)
        
    def draw(self, screen):
        #Only draw whats actually on camera
        for ladder in self.ladder_sprite_list:
            screen.blit(ladder.image, self.camera.apply(ladder))
        for door in self.door_sprite_list:
            screen.blit(door.image, self.camera.apply(door))
        for platform in self.platform_sprite_list:
            screen.blit(platform.image, self.camera.apply(platform))
        for monster in self.monster_sprite_list:
            screen.blit(monster.draw(), self.camera.apply(monster))
        for bullet in self.bullet_sprite_list:
            screen.blit(bullet.image, self.camera.apply(bullet))
        for player in self.player_sprite_list:
            screen.blit(player.draw(), self.camera.apply(player))
        for m_platform in self.moving_platforms_list:
            screen.blit(m_platform.draw(), self.camera.apply(m_platform))
        #always draw the UI
        for ui in self.ui_list:
            if ui['type'] == 'button':
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                rect = ui['rectangle']
                if rect.collidepoint(mouse[0], mouse[1]):
                    pygame.draw.rect(screen, ui['ac'],rect)
                    if click[0] == 1 and ui['action']!=None:
                        ui['action']()
                else:
                    pygame.draw.rect(screen, ui['ic'],rect)
            else:
                try:
                    screen.blit(ui['surface'],ui['rectangle'])
                except:
                    print(ui['type'])
                    raise
        if hasattr(self, 'ui_lifebar'):
            for lifebar in self.ui_lifebar:
                screen = lifebar[1].draw(screen)
        return screen

    # Giant Tree of Input parsing!

    def on_event(self, event):
        if self.menu_flag:
            self.menu_event(event)
        else:
            if hasattr(self, 'player'):
                self.game_event(event)
            else:
                print("Dropped Command.")
                    

    def menu_event(self, event):
        if event.type == pygame.QUIT:
           self._running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                #Left
                pass
            if event.key == K_RIGHT:
                #Right
                pass
            if event.key == K_UP:
                #Up
                pass
            if event.key == K_DOWN:
                #Down
                pass
            if event.key == ord('x'):
                #x
                pass
            if event.key == ord('z'):
                #z
                pass
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.exit_game()
            if event.key == K_LEFT:
                #Left
                self.main_menu.up()
                self.current_level = [self.main_menu.selected_name(), 0, 0, "R"]
            if event.key == K_RIGHT:
                #Right
                self.main_menu.down()
                self.current_level = [self.main_menu.selected_name(), 0, 0, "R"]
            if event.key == K_UP:
                #Up
                self.main_menu.up()
                self.current_level = [self.main_menu.selected_name(), 0, 0, "R"]
            if event.key == K_DOWN:
                #Down
                self.main_menu.down()
                self.current_level = [self.main_menu.selected_name(), 0, 0, "R"]
            if event.key == ord('z'):
                self.load_level(self.current_level)

    def game_event(self, event):
        if event.type == pygame.QUIT:
           self._running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.player.go_left()
            if event.key == K_RIGHT:
                self.player.go_right()
            if event.key == K_UP:
                self.player.go_up(self.ladder_sprite_list)
            if event.key == K_DOWN:
                self.player.go_down(self.ladder_sprite_list)
            if event.key == ord('x'):
                self.player.jump()
            if event.key == ord('z'):
                self.add_bullet(self.player.shoot())
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.exit_game()
            if event.key == K_LEFT:
                self.player.stop(self.ladder_sprite_list, 'left')
            if event.key == K_RIGHT:
                self.player.stop(self.ladder_sprite_list, 'right')
            if event.key == K_UP:
                self.player.stop(self.ladder_sprite_list, 'up')
            if event.key == K_DOWN:
                self.player.stop(self.ladder_sprite_list, 'down')
            if event.key == ord('x'):
                pass
            if event.key == ord('z'):
                self.player.stop_shoot()
            if event.key == ord('q'):
                if self._pause:
                    self.resume()
                else:
                    self.pause()
            if event.key == ord('r'):
                if self._debug:
                    self.main_menu.load_json()
                    self.load_level(self.current_level)
