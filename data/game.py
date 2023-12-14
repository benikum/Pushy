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
        
        self.compileMap()
        self.compileEntities()

        self.start_pos = self.validPosition(self.json_data["start"])
        self.finish_pos = self.validPosition(self.json_data["finish"])

    def validPosition(self, position):
        if not isinstance(position, list):
            return [0, 0]
        if len(position) != 2:
            return [0, 0]
        if position[0] < 0:
            position[0] = 0
        if position[0] > self.board_width:
            position[0] = self.board_width
        if position[1] < 0:
            position[1] = 0
        if position[1] > self.board_height:
            position[1] = self.board_height
        return position
    
    def compileMap(self):
        # loads level.json into a list with classes
        self.map = []
        raw_map = self.json_data["tile_map"]
        board = raw_map["map"]
        materials = raw_map["materials"]

        # error handling 
        if len(materials) == 0:
            materials = {"A":"sand"}
        while len(board) > self.board_height:
            board.pop(-1)
        while len(board) < self.board_height:
            board.append([])

        for row in board:
            # ["ABC"] -> ["A", "B", "C"]
            key_row = list(row)
            # ["AB"]  -> ["A", "B", "A"]
            while len(key_row) > self.board_width:
                key_row.pop(-1)
            while len(key_row) < self.board_width:
                key_row.append(list(materials.keys())[0])
            # ["A", "B", "C"] -> [matA, matB, matC]
            mat_row = []
            for tile in key_row:
                mat_row.append(StackController(materials[tile]))
            self.map.append(mat_row)
    
    def compileEntities(self):
        # loads entities from level.json into self.map
        self.entity_materials = {}
        if not "entities" in self.json_data:
            return
        for entity in self.json_data["entities"]:
            if not ("position" in entity) and ("id" in entity):
                continue
            position = self.validPosition(entity["position"])
            entity_id = entity["id"]
            if not entity_id in self.entity_materials:
                self.entity_materials[entity_id] = Entity(entity_id)
            self.map[position[1]][position[0]].addMaterial(self.entity_materials[entity_id])

    def moveEntity(self, current_pos, new_pos):
        current_stack = self.map[current_pos[1]][current_pos[0]]
        new_stack = self.map[new_pos[1]][new_pos[0]]
        if current_stack.entity == None or not new_stack.walkable:
            return current_pos
        new_stack.entity = current_stack.entity
        current_stack.entity = None
        return new_pos

class StackController():
    def __init__(self, base_material_id):
        self.materials[Material(base_material_id)]
    def addMaterial(self, material):
        self.materials.append(material)
    def getLayer(self):
        return self.layer if self.entity == None else self.layer + 1

class Material:
    def __init__(self, material_id):
        self.material_id = material_id
        self.material_path = "assets/materials/" + self.material_id + ".json"
        self.json_data = json_control.read(self.material_path)
        self.material_type = self.json_data["material_type"]

        self.texture = self.json_data["texture"]

class Entity(Material):
    def __init__(self, material_id):
        super().__init__(material_id)

        self.texture = self.json_data["texture"]
        # self.attributes = self.json_data["attributes"]

class PlayerEntity(Entity):
    def __init__(self, color):
        self.material_id = "player"
        super().__init__(self.material_id)
        
        self.color = color
        self.orientation = 0