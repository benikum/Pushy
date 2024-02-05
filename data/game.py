import sys
if __name__ == "__main__":
    sys.exit()

from data.file_ctrl import json_read

class LevelMapController:
    def __init__(self, level_id: str):
        # load map from level data
        self.id = level_id
        self.path = "assets/levels/" + self.id + ".json"
        self.data = json_read(self.path)
        
        self.level_name = self.data.get("name", self.id)

        self.map_width = self.data.get("width", 1)
        self.map_height = self.data.get("height", 1)
        
        self.start_pos = self.get_valid_pos(self.data.get("start", [0, 0]))
        self.finish_pos = self.get_valid_pos(self.data.get("finish", [0, 0]))
        
        self.load_map()

    def is_valid_pos(self, position: list):
        return isinstance(position, list) and len(position) == 2 \
        and (0 <= position[0] < self.map_width) \
        and (0 <= position[1] < self.map_height)

    def get_valid_pos(self, position: list):
        if self.is_valid_pos(position):
            return position
        return [0, 0]
    
    def set_length(self, data: list, lenght: int, filler = "A"):
        while len(data) > lenght:
            data.pop(-1)
        while len(data) < lenght:
            data.append(filler)
        return
    
    def load_map(self):
        # loads level.json into a list with classes
        raw_map = self.data.get("level", {})
        materials = raw_map.get("materials", {})
        
        base_map = self.set_length(raw_map.get("map", []), self.map_height)
        base_map = [self.set_length(list(item), self.map_width) for item in base_map]
        
        object_map = self.set_length(raw_map.get("objects", []), self.map_height)
        object_map = [self.set_length(list(item), self.map_width) for item in object_map]
        
        self.map = [StackController(materials.get(base_item, "water")) for base_item, object_item in zip(zip(base_map, object_map))]
            
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
    material_cache = {}
    def __init__(self, *material_ids: str):
        for id in material_ids:
            if id not in list(self.material_cache.keys()):
                self.material_cache[id] = Material(id)
        self.materials = [self.material_cache[item] for item in material_ids]
    def get_textures(self):
        return list([i.texture, i.orientation] for i in self.materials)
    #TODO 
    def get_entity_attributes(self):
        type_list = [i.material_type for i in self.materials]
        id_list = [i.material_id for i in self.materials]
        height_list = [i.height for i in self.materials]
        walk_list = [("walk" in i.attributes) for i in self.materials]
        move_list = [("move" in i.attributes) for i in self.materials]

        return type_list, id_list, height_list, walk_list, move_list

class Material:
    def __init__(self, material_id):
        self.id = material_id
        self.path = "assets/materials/" + self.id + ".json"
        self.data = json_read(self.path)

        # self.type = self.material_data.get("material_type", "block")
        self.texture = self.material_data.get("texture", "water")
        self.orientation = 0

        self.height = self.material_data.get("height", 0)
        self.attributes = self.material_data.get("attributes", [])