import sys
if __name__ == "__main__":
    sys.exit()

from data.file_ctrl import json_read

class LevelMapController:
    def __init__(self, map_id):
        self.map_id = map_id
        self.map_path = "assets/levels/" + self.map_id + ".json"
        self.json_data = json_read(self.map_path)
        
        self.level_name = self.json_data.get("name", "NAME")

        self.board_width = self.json_data.get("width", 1)
        self.board_height = self.json_data.get("height", 1)
        
        self.start_pos = self.get_valid_pos(self.json_data.get("start", [0, 0]))
        self.finish_pos = self.get_valid_pos(self.json_data.get("finish", [0, 0]))
        
        self.compile_map()
        self.compile_entities()

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
        raw_map = self.json_data.get("tile_map", {})
        board = raw_map.get("map", [])
        materials = raw_map.get("materials", {})

        # cut board height
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
                mat_row.append(StackController(materials.get(tile, "water")))
            self.map.append(mat_row)
        self.map[self.finish_pos[1]][self.finish_pos[0]].materials.append(Material("finish"))
    
    def compile_entities(self):
        # loads entities from level.json into self.map
        for entity in self.json_data.get("entities", []):
            # check if entity is valid
            if (not isinstance(entity, dict)) or (not ("position" in entity) and ("id" in entity)):
                continue
            position = self.get_valid_pos(entity["position"])
            entity_id = entity["material_id"]
            # add entity in stack
            self.map[position[1]][position[0]].materials.append(Material(entity_id))

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
        cur_entities = cur_stack.get_entity_attributes()
        new_entities = new_stack.get_entity_attributes()

        # cur_type = cur_entities[0]
        # cur_id = cur_entities[1]
        cur_height = cur_entities[2]
        # cur_walk = cur_entities[3]
        cur_move = cur_entities[4]

        # new_type = new_entities[0]
        # new_id = new_entities[1]
        new_height = new_entities[2]
        new_walk = new_entities[3]
        new_move = new_entities[4]
        
        if sum(new_height) <= (sum(cur_height) - cur_height[-1]) and new_walk[-1]:
            new_stack.materials.append(cur_stack.materials[-1])
            cur_stack.materials.pop(-1)
            return new_pos
        if (sum(new_height)-new_height[-1]) == (sum(cur_height) - cur_height[-1]) \
        and new_height[-1] == cur_height[-1] \
        and new_walk[-2] \
        and new_move[-1] and cur_move[-1]:
            far_pos = [new_pos[0] + rel_pos[0], new_pos[1] + rel_pos[1]]
            if self.is_valid_pos(far_pos):
                far_stack = self.map[far_pos[1]][far_pos[0]]
                far_entities = far_stack.get_entity_attributes()

                # far_type = far_entities[0]
                # far_id = far_entities[1]
                far_height = far_entities[2]
                # far_walk = far_entities[3]
                # far_move = far_entities[4]
                
                # if box can move to far_stack
                if sum(far_height) <= (sum(new_height) - new_height[-1]):
                    # move box
                    far_stack.materials.append(new_stack.materials[-1])
                    new_stack.materials.pop(-1)
                    # move player
                    new_stack.materials.append(cur_stack.materials[-1])
                    cur_stack.materials.pop(-1)
                    return new_pos
        return cur_pos
    
    def event_listener(self):
        events = []
        if "player" in [i.material_type for i in self.map[self.finish_pos[1]][self.finish_pos[0]].materials]:
            events.append("win")
        return events

class StackController():
    def __init__(self, material_id):
        self.materials = [Material(material_id)]
        self.listener = []
    def get_textures(self):
        return list([i.texture, i.orientation] for i in self.materials)
    def get_entity_attributes(self):
        type_list = [i.material_type for i in self.materials]
        id_list = [i.material_id for i in self.materials]
        height_list = [i.height for i in self.materials]
        walk_list = [("walk" in i.attributes) for i in self.materials]
        move_list = [("move" in i.attributes) for i in self.materials]

        return type_list, id_list, height_list, walk_list, move_list

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