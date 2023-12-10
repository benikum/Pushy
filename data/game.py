# import pygame
from data import json_control

class LevelMapController:
    def __init__(self, map_id):
        self.map_path = "assets/level/" + map_id + ".json"
        self.json_data = json_control.read(self.map_path)
        
        # read infomation
        self.level_name = self.json_data["name"]

        self.board_width = self.json_data["width"]
        self.board_height = self.json_data["height"]

        self.start_pos = self.json_data["start"]
        self.finish_pos = self.json_data["finish"]

        self.raw_map = self.json_data["map"]
        self.objects = self.json_data["objects"]

class Tile:
    def __init__(self, material):
        self.material_path = "assets/materials/" + material + ".json"
        self.json_data = json_control.read(self.material_path)

        self.object = None
        self.walkable = True
    def addObject(self, material):
        self.object_path = "assets/materials/" + material + ".json"
        self.json_data = json_control.read(self.object_path)
    def popObject(self):
        self.object = None
        return #informationen