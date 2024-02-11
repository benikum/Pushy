import sys
if __name__ == "__main__":
    sys.exit()

from data.file_ctrl import JSONReadError, InstanceCache, json_read

class JSONFileCorrupt(Exception):
    def __init__(self, msg="JSON file has missing data"):
        self.msg = msg
        super().__init__(self.msg)

class LevelMapController:
    def __init__(self, level_id: str):
        # load map from level data
        self.id = level_id
        path = "assets/levels/" + self.id + ".json"
        try:
            self.data = json_read(path)
        except JSONReadError:
            raise JSONFileCorrupt("Cannot read JSON file: " + path)
        
        try:
            self.level_name = self.data["name"]
            self.map_width = self.data["width"]
            self.map_height = self.data["height"]
        except KeyError:
            raise JSONFileCorrupt("Level File has missing data")
        
        self.game_events = []
        
        self.load_map()

    def is_valid_pos(self, position):
        return (0 <= position[0] < self.map_width) and (0 <= position[1] < self.map_height)
        
    def load_map(self):
        # loads level.json into a list
        try:
            raw_map: dict = self.data["level"]
            materials: dict = raw_map["materials"]
            
            base_map = [list(row) for row in raw_map["map"]]
            object_map = [list(item) for item in raw_map["objects"]]
        except KeyError:
            raise JSONFileCorrupt("Level file has missing map data")
        
        # checks if map data is the same 
        if len(base_map) != self.map_height or len(object_map) != self.map_height:
            raise JSONFileCorrupt("Map height invalid")
        if any(len(row) != self.map_width for row in base_map) or any(len(row) != self.map_width for row in object_map):
            raise JSONFileCorrupt("Map width invalid")
        
        try:
            self.map = [[StackController(materials[item]) for item in row] for row in base_map]
        except KeyError as ke:
            raise JSONFileCorrupt("Missing material key: " + str(ke))
        
        for y, base_map_row, object_row in zip(range(self.map_height), self.map, object_map):
            for x, item, object_id in zip(range(self.map_width), base_map_row, object_row):
                # nothing there
                if object_id == "-":
                    continue
                elif object_id == next(key for key, value in materials.items() if value == "start"):
                    self.start_pos = (x, y)
                    continue
                elif object_id == next(key for key, value in materials.items() if value == "finish"):
                    self.finish_pos = (x, y)
                item.materials.append(StackController.material_cache.load_key(materials[object_id]))

    def move_player(self, cur_pos, rel_pos):
        # check if valid
        if not self.is_valid_pos(cur_pos):
            return [0, 0]
        new_pos = [cur_pos[0] + rel_pos[0], cur_pos[1] + rel_pos[1]]
        if not self.is_valid_pos(new_pos):
            print("new_pos invalid")
            return cur_pos
        
        # get StackController instances
        cur_stack = self.map[cur_pos[1]][cur_pos[0]]
        new_stack = self.map[new_pos[1]][new_pos[0]]

        if (sum([item.height for item in cur_stack.materials]) - cur_stack.materials[-1].height) >= sum(item.height for item in new_stack.materials) \
        and ("walk" in new_stack.materials[-1].attributes):
            # move the player
            new_stack.materials.append(cur_stack.materials[-1])
            cur_stack.materials.pop(-1)
            return new_pos
        # far_pos = [cur_pos[0] + rel_pos[0] * 2, cur_pos[1] + rel_pos[1] * 2]
        # far_stack = self.map[far_pos[1]][far_pos[0]]
        return cur_pos
    
    def event_manager(self):
        pass

class Material:
    def __init__(self, material_id):
        self.id = material_id
        path = "assets/materials/" + self.id + ".json"
        
        try:
            self.data = json_read(path)
        except JSONReadError:
            raise JSONFileCorrupt("Cannot read JSON file: " + path)
        
        try:
            self.type = self.data["type"]
            self.texture = self.data["texture"]
            self.height = self.data["height"]
        except KeyError as ke:
            raise JSONFileCorrupt("Missing material data: " + str(ke) + " / " + path)

        self.attributes = self.data.get("attributes", [])
        self.events = self.data.get("events", [])

class StackController():
    material_cache = InstanceCache(Material)
    def __init__(self, material_id: str):
        self.materials = [self.material_cache.load_key(material_id)]
        
    def get_textures(self):
        return list(item.texture for item in self.materials if item.type != "player")