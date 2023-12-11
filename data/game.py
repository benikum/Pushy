# import pygame
from data import json_control

class LevelMapController:
    def __init__(self, map_id):
        self.map_id = map_id
        self.map_path = "assets/levels/" + self.map_id + ".json"
        self.json_data = json_control.read(self.map_path)
        
        # read infomation
        self.level_name = self.json_data["name"]

        self.board_width = self.json_data["width"]
        self.board_height = self.json_data["height"]

        self.start_pos = self.json_data["start"]
        self.finish_pos = self.json_data["finish"]

        self.compileMap()
        self.compileEntities()
    def compileMap(self):
        # clear current map
        self.map = []
        raw_map = self.json_data["tile_map"]
        board = raw_map["map"]
        materials = raw_map["materials"]
        if len(board) != self.board_height:
            #asduhbasd
            pass
        for row in board:
            row = list(row)
            temp_row = []
            for tile in row:
                temp_row.append(StackController(materials[tile]))
            self.map.append(temp_row)
    def compileEntities(self):
        for entity in self.json_data["entities"]:
            pos_x, pos_y = entity["position"]
            self.map[pos_y][pos_x].setEntity(entity["type"])
    def moveEntity(self, current_pos, new_pos):
        current_stack = self.map[current_pos[1]][current_pos[0]]
        new_stack = self.map[new_pos[1]][new_pos[0]]
        if current_stack.entity == None or new_stack.entity != None:
            return False
        new_stack.entity = current_stack.entity
        current_stack.delEntity()
        return True

class Material:
    def __init__(self, material_id):
        self.material_id = material_id
        self.material_path = "assets/materials/" + self.material_id + ".json"
        self.json_data = json_control.read(self.material_path)
        self.material_type = self.json_data["material_type"]

class StackController(Material):
    def __init__(self, material_id):
        super().__init__(material_id)

        self.texture = self.json_data["texture"]
        self.walkable = self.json_data["walkable"]
        self.layer = self.json_data["layer"]
        self.entity = None
    def setEntity(self, material_id):
        self.entity = Entity(material_id)
    def delEntity(self):
        self.entity = None
    def getTexture(self):
        return self.texture if self.entity == None else self.entity.texture
    def getLayer(self):
        return self.layer if self.entity == None else self.layer + 1

class Entity(Material):
    def __init__(self, material_id):
        super().__init__(material_id)

        self.texture = self.json_data["texture"]
        # self.attributes = self.json_data["attributes"]

class Player(Entity):
    def __init__(self, material_id, color):
        super().__init__(material_id)
        
        self.color = color
        self.orientation = 0