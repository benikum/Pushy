import json
class LevelMapController:
    def __init__(self, map_id):
        self.map_id = map_id
        self.map_path = "assets/levels/" + self.map_id + ".json"
        with open(self.map_path, "r") as file:
            self.json_data = json.load(file)
        
        # read infomation
        self.level_name = self.json_data["name"]

        self.board_width = self.json_data["width"]
        self.board_height = self.json_data["height"]
        
        self.compileMap()
        self.compileEntities()

        self.start_pos = self.getValidPos(self.json_data["start"])
        self.finish_pos = self.getValidPos(self.json_data["finish"])

    def isValidPos(self, position):
        return isinstance(position, list) and len(position) == 2 \
        and (0 <= position[0] < self.board_width) \
        and (0 <= position[1] < self.board_height)

    def getValidPos(self, position):
        if self.isValidPos(position):
            return position
        return [0, 0]
    
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
            position = self.getValidPos(entity["position"])
            entity_id = entity["id"]
            if not entity_id in self.entity_materials:
                self.entity_materials[entity_id] = Entity(entity_id)
            self.map[position[1]][position[0]].addMaterial(self.entity_materials[entity_id])

    def moveEntity(self, material_id , current_pos, rel_pos):
        # return if invalid
        if not self.isValidPos(current_pos):
            return [0, 0]
        
        if (not (isinstance(rel_pos, list) and len(rel_pos) == 2)) or rel_pos.count(0) == 2:
            return current_pos
        
        new_pos = [current_pos[0] + rel_pos[0], current_pos[1] + rel_pos[1]]
        if not self.isValidPos(new_pos):
            return current_pos
        
        # get StackController instances
        current_stack = self.map[current_pos[1]][current_pos[0]]
        new_stack = self.map[new_pos[1]][new_pos[0]]

        current_layers = current_stack.getLayers()
        new_layers = new_stack.getLayers()

        new_walkables = new_stack.getWalkables()

        # step to next top
        if new_walkables[-1] and new_layers[-1] <= current_layers[-2]:
            # move player
            new_stack.addMaterial(current_stack.getMaterial(material_id))
            current_stack.delMaterial(material_id)
            return new_pos
        
        # step to next block and move box
        if len(new_walkables) > 1 and new_walkables[-2] and new_layers[-1] == current_layers[-1]:
            # calculate far_stack
            far_pos = [new_pos[0] + rel_pos[0], new_pos[1] + rel_pos[1]]
            if self.isValidPos(far_pos):
                far_stack = self.map[far_pos[1]][far_pos[0]]
                far_layers = far_stack.getLayers()
                # if box can move to far_stack
                if new_layers[-2] <= far_layers[-1]:
                    # move box
                    far_stack.addMaterial(new_stack.materials[-1])
                    far_stack.materials.pop(-1)
                    # move player
                    new_stack.addMaterial(current_stack.getMaterial(material_id))
                    current_stack.delMaterial(material_id)
                    return new_pos
        return current_pos

class StackController():
    def __init__(self, material_id):
        self.materials = [Material(material_id)]
    def addMaterial(self, material):
        self.materials.append(material)
    def delMaterial(self, mat_id):
        id_list = list(i.material_id for i in self.materials)
        for i, m in enumerate(id_list):
            if mat_id == m:
                if i != 0:
                    self.materials.pop(i)
        return False
    def getMaterial(self, mat_id):
        id_list = list(i.material_id for i in self.materials)
        for i, m in enumerate(id_list):
            if mat_id == m:
                return self.materials[i]
    def getTextures(self):
        return list([i.texture, i.orientation if isinstance(i, PlayerEntity) else 0] for i in self.materials)
    def getWalkables(self):
        return list("walk" in i.attributes for i in self.materials)
    def getLayers(self):
        return list(i.height for i in self.materials)
            
class Material:
    def __init__(self, material_id):
        self.material_id = material_id
        self.material_path = "assets/materials/" + self.material_id + ".json"
        try:
            with open(self.material_path, "r") as file:
                self.json_data = json.load(file)
        except FileNotFoundError:
            self.material_type = "error"
            self.texture = "error"
            self.height = 0
            self.attributes = []
            return
        self.material_type = self.json_data["material_type"]
        self.texture = self.json_data["texture"]
        self.height = self.json_data["height"]
        self.attributes = self.json_data["attributes"]

class PlayerEntity(Material):
    def __init__(self, color):
        super().__init__("player")
        self.color = color
        self.orientation = 0

class Entity(Material):
    def __init__(self, material_id):
        super().__init__(material_id)

# test = StackController("sand")
# print("\n\n")
# print(test.getTextures())
# print(test.getWalkables())
# print(test.getLayers())
# print(test.getMaterial("player"))
# test.addMaterial(PlayerEntity("green"))
# print("\n")
# print(test.getTextures())
# print(test.getWalkables())
# print(test.getLayers())
# print(test.getMaterial("player"))