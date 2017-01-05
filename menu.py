from text import Text
from os import listdir
import json, constants

class Menu:
    def __init__(self):
        self.level_json_list = {}
        self.level_list = []
        self.completed = {}
        self.icon_list = {}
        self.menu_item = 0
        self.load_json()
        if len(self.level_list) > 0:
            self.selected = self.level_list[0]
        
    def get_level_json(self, level):
        return self.level_json_list[level]

    def draw_menu(self, surface):
        pass

    def load_json(self):
        files = listdir("levels")
        for file in files:
            with open("levels\\"+file) as data_file:
                data = json.load(data_file)
                self.level_json_list[data['name']] = data
                if 'start' in data:
                    if data['start'] == 'True':
                        self.level_list.append(data['name'])
                        self.completed[data['name']] = False
                        #icon = self.load_icon(data['menu_tile'])
                        #self.icon_list[data['name']] = icon
                else:
                    print(data['name'], "No start")

    def load_icon(self, icon_file):
        pass

    def draw_menu(self):
        menu = []
        #add the menu options
        for x in range(len(self.level_list)):
            text = self.level_list[x]
            TextSurf, TextRect = Text.text_objects(text, constants.menuText,
                                                   constants.WHITE)
            TextRect.center = ((constants.DWIDTH / 4), (100+(x*50)))
            menu.append({'title': text, 'type':'menu',
                         'surface':TextSurf, 'rectangle': TextRect})
        #add the menu icon
        #IconRect = Rect((constants.DWIDTH*.75), (constants.DHEIGHT/4), 100, 100)
        #menu.append({'type':'icon', 'title':'Level_Icon', 'rectangle':IconRect})
        return menu

    def selected_name(self):
        name = self.level_list[self.menu_item]
        return name

    def fetch_icon(self, name):
        return self.icon_list[name]

    def finished_level(self, name):
        if name in self.completed.keys():
            self.completed[name] = True

    def boss_check(self, name):
        if name in self.completed.keys():
            return self.completed[name]
        else:
            print("Couldn't find the key")
            return False

    def up(self):
        if self.menu_item > 0:
            self.menu_item -= 1
        return True

    def down(self):
        if self.menu_item < len(self.level_list)-1:
            self.menu_item +=1
        return True
         
class Game_Menu:
    def __init__(self):
        pass
