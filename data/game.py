from os import walk
from data.file_ctrl import json_read

class LevelMapController:
    def __init__(self, map_id):
        self.map_id = map_id
        self.map_path = "assets/levels/" + self.map_id + ".json"
        self.json_data = json_read(self.map_path)
        
        self.level_name = self.json_data.get("name", "NAME")

        self.board_width = self.json_data.get("width", 1)
        self.board_height = self.json_data.get("height", 1)
        
        self.compile_map()
        self.compile_entities()

        self.start_pos = self.get_valid_pos(self.json_data.get("start", [0, 0]))
        self.finish_pos = self.get_valid_pos(self.json_data.get("finish", [0, 0]))

    def is_valid_pos(self, position):
        return isinstance(position, list) and len(position) == 2 \
        and (0 <= position[0] < self.board_width) \
        and (0 <= position[1] < self.board_height)

    def get_valid_pos(self, position):
        if self.is_valid_pos(position):
            return position
        return [0, 0]
    
    def compile_map(self):
        # loads level.json into a list with classes
        self.map = []
        raw_map = self.json_data["tile_map"]
        board = raw_map["map"]
        materials = raw_map["materials"]

        # cut board height
        if len(materials) == 0:
            materials = {"A":"sand"}
        while len(board) > self.board_height:
            board.pop(-1)
        while len(board) < self.board_height:
            board.append([])

        for row in board:
            # cut board width
            key_row = list(row)
            while len(key_row) > self.board_width:
                key_row.pop(-1)
            while len(key_row) < self.board_width:
                key_row.append(list(materials.keys())[0])
            # convert index to stackcontroller
            mat_row = []
            for tile in key_row:
                mat_row.append(StackController(materials[tile]))
            self.map.append(mat_row)
    
    def compile_entities(self):
        # loads entities from level.json into self.map
        self.entity_materials = dict()
        for entity in self.json_data.get("entities", []):
            # check if entity is valid
            if (not isinstance(entity, dict)) or (not ("position" in entity) and ("id" in entity)):
                continue
            position = self.get_valid_pos(entity["position"])
            entity_id = entity["material_id"]
            if not entity_id in self.entity_materials:
                self.entity_materials[entity_id] = Material(entity_id)
            # add entity in stack
            self.map[position[1]][position[0]].materials.append(self.entity_materials[entity_id])

    def move_entity(self, material_id, cur_pos, rel_pos):
        # check if valid
        if not self.is_valid_pos(cur_pos):
            return [0, 0]
        if (not (isinstance(rel_pos, list) and len(rel_pos) == 2)) or rel_pos.count(0) == 2:
            return cur_pos
        new_pos = [cur_pos[0] + rel_pos[0], cur_pos[1] + rel_pos[1]]
        if not self.is_valid_pos(new_pos):
            return cur_pos
        
        # get StackController instances
        cur_stack = self.map[cur_pos[1]][cur_pos[0]]
        new_stack = self.map[new_pos[1]][new_pos[0]]

        # parallel lists
        cur_type, cur_id, cur_height, cur_walk = cur_stack.get_entity_attributes()
        new_type, new_id, new_height, new_walk = new_stack.get_entity_attributes()
        
        # cur_material_layer = -1
        # for i, id in enumerate(cur_id):
        #     if id == material_id:
        #         cur_material_layer = i
        #         break
        # print(cur_height, new_height, cur_id, new_id, cur_material_layer, sum(cur_height[:cur_material_layer]))
        # print(cur_material_layer)
        # das material soll auf den new_stack verschobenw werden, wenn die höhe der material_id größer gleich von dem maximalen höhe des new_stack ist
        if sum(new_height) <= (sum(cur_height)-cur_height[-1]) and new_walk[-1]:
            new_stack.materials.append(cur_stack.materials[-1])
            cur_stack.materials.pop(-1)
            return new_pos
        if (sum(new_height)-new_height[-1]) == (sum(cur_height)-cur_height[-1]) and new_height[-1] == cur_height[-1] and new_walk[-2]:
            far_pos = [new_pos[0] + rel_pos[0], new_pos[1] + rel_pos[1]]
            if self.is_valid_pos(far_pos):
                far_stack = self.map[far_pos[1]][far_pos[0]]
                far_type, far_id, far_height, far_walk = far_stack.get_entity_attributes()
                
                # if box can move to far_stack
                if sum(far_height) <= (sum(new_height)-new_height[-1]):
                    # move box
                    far_stack.materials.append(new_stack.materials[-1])
                    new_stack.materials.pop(-1)
                    # move player
                    new_stack.materials.append(cur_stack.materials[-1])
                    cur_stack.materials.pop(-1)
                    return new_pos
        return cur_pos

class StackController():
    def __init__(self, material_id):
        self.materials = [Material(material_id)]
    def get_textures(self):
        return list([i.texture, i.orientation] for i in self.materials)
    def get_entity_attributes(self):
        type_list = [i.material_type for i in self.materials]
        id_list = [i.material_id for i in self.materials]
        height_list = [i.height for i in self.materials]
        walk_list = [("walk" in i.attributes) for i in self.materials]

        return type_list, id_list, height_list, walk_list

class Material:
    def __init__(self, material_id):
        self.material_id = material_id
        self.material_path = "assets/materials/" + self.material_id + ".json"
        self.json_data = json_read(self.material_path)

        self.material_type = self.json_data.get("material_type", "block")
        self.texture = self.json_data.get("texture", "water")
        self.orientation = 0

        self.height = self.json_data.get("height", 0)
        self.attributes = self.json_data.get("attributes", [])