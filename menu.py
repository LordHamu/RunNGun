from text import Text
from os import listdir
import json, constants

class Menu:
    def __init__(self):
        self.level_json_list = {}
        self.level_list = []
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
                else:
                    print(data['name'], "No start")

    def draw_text(self, text, x, y):
        TextSurf, TextRect = Text.text_objects(title, constants.largeText, constants.WHITE)
        TextRect.center = (x, y)
        self.ui_list.append({'title':title, 'type': 'text','surface':TextSurf,'rectangle':TextRect})

class Game_Menu:
    def __init__(self):
        pass
