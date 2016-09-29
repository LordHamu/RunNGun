from os import listdir
import json

class Menu:
    def __init__(self):
        self.level_json_list = {}
        self.level_list = []
        self.load_json()
        
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
                self.level_list.append(data['name'])
