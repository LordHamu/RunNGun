"""
Basic Shooter: Game
Author: Clayton Headley
Description: This contains all the game logic, I seperated it from the pygame
runner so that main stays uncluttered.
"""

import pygame, constants, sys, copy, json
from pygame.locals import *
from player import Player
from monster import Monster
from camera import Camera
from level import Level, Platform, Bullet
from text import Text
from menu import Menu
from hpbar import Lifebar
from pawn import Pawn
from os import listdir

class Game:

    def __init__(self):
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
        self.object_list = {}
        self.create_objects()
        self.ui_list = []
        self.load_menu()

    #GAME
    def load_menu(self):
        self.clear()
        self.add_title("Run & Gun")
        self.add_button("New",(constants.DWIDTH/2)-50, 350, 100,50,
                        constants.WHITE, constants.BLUE, self.start_game)
        self.add_button("Quit",(constants.DWIDTH/2)-50, 450, 100,50,
                        constants.WHITE, constants.BLUE, self.exit_game)

    def start_game(self):
        self.clear()
        self.lives = 3
        self.game_menu = Menu()
        self.current_level = ['Mario 1-3', 0, 0, "R"]
        self.load_level(self.current_level)
        
    def exit_game(self):
        pygame.quit()
        sys.exit()

    def load_level(self, level):
        self.clear()
        self.level = Level(self.game_menu.get_level_json(level[0]))
        if level[1] != 0:
            self.level.player_x = level[1]
        if level[2] != 0:
            self.level.player_y = level[2]
        self.scenery_sprite_list = self.level.build_scenery()
        self.platform_sprite_list = self.level.build_platforms()
        self.ladder_sprite_list = self.level.build_ladders()
        self.door_sprite_list = self.level.build_doors()
        self.spawners = self.level.build_spawners()
        self.backdrop = self.level.backdrop
        self.add_player(self.character, self.level.player_x, self.level.player_y, level[3])
        self.add_camera()
        self.add_lifebar(25, 25, self.player.get_max_life())

    def reload_level(self):
        self.clear()
        self.scenery_sprite_list = self.level.build_scenery()
        self.platform_sprite_list = self.level.build_platforms()
        self.ladder_sprite_list = self.level.build_ladders()
        self.backdrop = self.level.backdrop
        self.add_player(self.character, self.level.player_x, self.level.player_y, "R")
        self.add_camera()
        self.add_lifebar(25, 25, self.player.get_max_life())

    #Add functions
    def add_camera(self):
        self.camera = Camera(self.level.width, self.level.height)

    def add_lifebar(self, x, y, hp):
        self.lifebar = Lifebar( x, y, 20, 200, True)
        self.lifebar.set_hp(hp)
        
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

    def add_monster(self, file, x, y):
        monster = Monster(file, ['U','L','D'], 10)
        monster.rect.x = x
        monster.rect.y = y
        if self.monster_sprite_list.has(monster):
            print("Dupe Monster added.")
            return False
        else:
            self.monster_sprite_list.add(copy.copy(monster))
        return True

    def add_bullet(self, cord):
        bullet = Bullet(self.level.rect)
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
        pawn = Pawn(pawn_file)
        pawn.rect.x = cord[0]
        pawn.rect.y = cord[1]
        pawn.set_movement(move[0], move[1])
        self.moving_platforms_list.add(pawn)
        return True
        
    def add_player(self, json, x, y, d):
        self.player = Player(json)
        self.player.rect.x = x
        self.player.rect.y = y
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
        if hasattr(self, 'lifebar'):
            del self.lifebar
        if hasattr(self, 'player'):
            del self.player

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    def character_death(self):
        if self.lives > 0:
            self.lives += -1
            self.player.refresh()
            self.level.refresh()
            self.reload_level()
        else:
            self.clear
            self.load_menu

    def change_level(self):
        change = False
        hits_list = pygame.sprite.spritecollide(self.player, self.door_sprite_list, False)
        for hit in hits_list:
            self.current_level = [hit.level, hit.px, hit.py, hit.dir]
            change = True
        return change

    def check_dead(self):
        return False
        
    #Pygame functions
        
    def update(self):
        if not (self._pause) and hasattr(self, 'player'):
            self.moving_platforms_list.update(self.player_sprite_list)
            self.player_sprite_list.update(self.monster_sprite_list.sprites(),
                                           self.platform_sprite_list,
                                           self.moving_platforms_list)
            self.monster_sprite_list.update(self.bullet_sprite_list.sprites())
            self.bullet_sprite_list.update()
            if self.change_level():
                self.load_level(self.current_level)
            if self.check_dead():
                self.character_death()
        if hasattr(self, 'camera'):
            self.camera.update(self.player)
        if hasattr(self, 'lifebar'):
            self.lifebar.update(self.player)
        for spawner in self.spawners:
            spawn = spawner.update()
            if spawn == False:
                pass
            elif spawn[0] == "Platform":
                pawn_type = self.object_list[spawn[1]]
                self.add_platform(pawn_type,
                                  spawn[2],
                                  spawn[3])
            else:
                pass
        
        
    def draw(self, screen):
        #Only draw whats actually on camera
        for ladder in self.ladder_sprite_list:
            screen.blit(ladder.image, self.camera.apply(ladder))
        for door in self.door_sprite_list:
            screen.blit(door.image, self.camera.apply(door))
        for platform in self.platform_sprite_list:
            screen.blit(platform.image, self.camera.apply(platform))
        for monster in self.monster_sprite_list:
            screen.blit(monster.image, self.camera.apply(monster))
        for bullet in self.bullet_sprite_list:
            screen.blit(bullet.image, self.camera.apply(bullet))
        for player in self.player_sprite_list:
            screen.blit(player.draw(), self.camera.apply(player))
        for m_platform in self.moving_platforms_list:
            screen.blit(m_platform.draw(), self.camera.apply(m_platform))
        #all ways draw the UI
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
                screen.blit(ui['surface'],ui['rectangle'])
        if hasattr(self, 'lifebar'):
            screen = self.lifebar.draw(screen)
        return screen

    # Giant Tree of Input parsing!

    def on_event(self, event):
        if event.type == pygame.QUIT:
           self._running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if hasattr(self, 'player'):
                    self.player.go_left()
            if event.key == K_RIGHT:
                if hasattr(self, 'player'):
                    self.player.go_right()
            if event.key == K_UP:
                if hasattr(self, 'player'):
                    self.player.go_up(self.ladder_sprite_list)
            if event.key == K_DOWN:
                if hasattr(self, 'player'):
                    self.player.go_down(self.ladder_sprite_list)
            if event.key == ord('x'):
                if hasattr(self, 'player'):
                    self.player.jump()
            if event.key == ord('z'):
                if hasattr(self, 'player'):
                    self.add_bullet(self.player.shoot())
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                    self.exit_game()
            if event.key == K_LEFT:
                if hasattr(self, 'player'):
                    self.player.stop(self.ladder_sprite_list, 'left')
            if event.key == K_RIGHT:
                if hasattr(self, 'player'):
                    self.player.stop(self.ladder_sprite_list, 'right')
            if event.key == K_UP:
                if hasattr(self, 'player'):
                    self.player.stop(self.ladder_sprite_list, 'up')
            if event.key == K_DOWN:
                if hasattr(self, 'player'):
                    self.player.stop(self.ladder_sprite_list, 'down')
            if event.key == ord('x'):
                pass
            if event.key == ord('z'):
                if hasattr(self, 'player'):
                    self.player.stop_shoot()
            if event.key == ord('q'):
                if self._pause:
                    self.resume()
                else:
                    self.pause()
            if event.key == ord('r'):
                self.game_menu.load_json()
                self.load_level(self.current_level)
