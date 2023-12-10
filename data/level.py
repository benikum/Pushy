# import pygame
import json

class LevelController:
    def __init__(self, map_id):
        self.map_path = "assets/level/" + map_id + ".json"
        with open(self.map_path, "r") as file:
            self.level_data = json.load(file)
        
        # read infomation
        self.level_name = self.level_data["name"]

        self.board_width = self.level_data["width"]
        self.board_height = self.level_data["height"]

        self.start_pos = self.level_data["start"]
        self.finish_pos = self.level_data["finish"]

        self.raw_map = self.level_data["map"]
        self.objects = self.level_data["objects"]

class Tile:
    def __init__(self, material):
        self.material_path = "assets/materials/" + material + ".json"
        with open(self.material_path, "r") as file:
            self.level_data = json.load(file)
        
        self.object = None
        self.walkable = True
    def addObject(self):
        pass
    def popObject(self):
        self.object = None
        return #informationen