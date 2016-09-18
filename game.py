"""
Basic Shooter: Game
Author: Clayton Headley
Description: This contains all the game logic, I seperated it from the pygame
runner so that main stays uncluttered.
"""

import pygame, constants, sys, copy
from pygame.locals import *
from player import Player
from monster import Monster
from camera import Camera
from level import Platform, Bullet, Level
from text import Text
from menu import Menu

class Game:

    def __init__(self):
        self._pause = False
        self.backdrop = constants.BLACK
        self.monster_sprite_list = pygame.sprite.Group()
        self.bullet_sprite_list = pygame.sprite.Group()
        self.player_sprite_list = pygame.sprite.Group()
        self.platform_sprite_list = pygame.sprite.Group()
        self.ladder_sprite_list = pygame.sprite.Group()
        self.ui_list = []
        self.load_menu()

    #GAME
    def load_menu(self):
        self.clear()
        self.add_title("Run & Gun")
        self.add_button("New",(constants.DWIDTH/2)-50, 350, 100,50,
                        constants.WHITE, constants.BLUE, self.load_game)
        self.add_button("Quit",(constants.DWIDTH/2)-50, 450, 100,50,
                        constants.WHITE, constants.BLUE, self.exit_game)

    def load_game(self):
        self.clear()
        self.game_menu = Menu()
        self.load_level('Mario 1-1')
        

    def load_level(self, level):
        self.clear()
        self.add_level(level)
        self.add_camera()
        
    def exit_game(self):
        pygame.quit()
        sys.exit()

    #Add functions

    def add_level(self, level):
        self.level = Level(self.game_menu.get_level_json(level))
        self.platform_sprite_list = self.level.build_platforms()
        self.ladder_sprite_list = self.level.build_ladders()
        self.backdrop = self.level.backdrop
        self.add_player("json\\megaman.json", self.level.player_x, self.level.player_y)

    def add_camera(self):
        self.camera = Camera(self.level.width, self.level.height)
    
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

    def add_object(self, obj_name, x, y):
        obj = self._bg_object.get_object(obj_name)
        if not(obj):
            print("could not find key pair:" + obj_name)
        else:
            obj.rect.x = x
            obj.rect.y = y
            self.level_sprite_list.add(obj)
        
    def add_player(self, json, x, y):
        self.player = Player(json)
        self.player.rect.x = x
        self.player.rect.y = y
        self.player_sprite_list.add(self.player)
    
    #Helper functions

    def clear(self):
        self.ui_list = []
        self.level_sprite_list = pygame.sprite.Group()
        self.monster_sprite_list = pygame.sprite.Group()
        self.player_sprite_list = pygame.sprite.Group()
        self.bullet_sprite_list = pygame.sprite.Group()

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    #Pygame functions
        
    def update(self):
        #print(len(self.active_sprite_list)) //Used to check number of objects floating around.
        if not (self._pause):
            #self.level_sprite_list.update()
            self.player_sprite_list.update(self.monster_sprite_list.sprites(),
                                           self.platform_sprite_list,
                                           self.ladder_sprite_list)
            self.monster_sprite_list.update(self.bullet_sprite_list.sprites())
            self.bullet_sprite_list.update()
        if hasattr(self, 'camera'):
            self.camera.update(self.player)

    def draw(self, screen):
        #Only draw whats actually on camera
        for ladder in self.ladder_sprite_list:
            screen.blit(ladder.image, self.camera.apply(ladder))
        for platform in self.platform_sprite_list:
            screen.blit(platform.image, self.camera.apply(platform))
        for monster in self.monster_sprite_list:
            screen.blit(monster.image, self.camera.apply(monster))
        for bullet in self.bullet_sprite_list:
            screen.blit(bullet.image, self.camera.apply(bullet))
        for player in self.player_sprite_list:
            screen.blit(player.draw(), self.camera.apply(player))
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
                    self.player.stop(self.ladder_sprite_list)
            if event.key == K_RIGHT:
                if hasattr(self, 'player'):
                    self.player.stop(self.ladder_sprite_list)
            if event.key == K_UP:
                if hasattr(self, 'player'):
                    self.player.stop(self.ladder_sprite_list)
            if event.key == K_DOWN:
                if hasattr(self, 'player'):
                    self.player.stop(self.ladder_sprite_list)
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
