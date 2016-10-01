import pygame, json

class Spawner:
    def __init__(self, json):
        self.type = json['type']
        self.sprite = json['sprite']
        self.x = json['x']*50
        self.y = json['y']*50
        self.speed_x = json['speed']['x']
        self.speed_y = json['speed']['y']
        if "path" in json:
            self.path = json['path']
            self.path_speed = json['speed']['path']
        self.limit = int(json['limit'])
        if self.limit < 0:
            self.unlimited = True
        else:
            self.unlimited = False
        self.frequency = int(json['freq'])
        self.tick = 0
        self.spawn = 0

    def update(self):
        if self.tick > self.frequency:
            self.tick = 0
            s = self.test_spawn()
            return s
        else:
            self.tick += 1
            return False

    def test_spawn(self):
        arr = ["Nope", "Nope", [0,0], [0,0]]
        if self.unlimited:
            arr = [self.type,
                    self.sprite,
                    [self.x, self.y],
                    [self.speed_x, self.speed_y]]
        elif self.spawn < self.limit:
            self.spawn += 1
            arr = [self.type,
                    self.sprite,
                    [self.x, self.y],
                    [self.speed_x, self.speed_y]]
        return arr
