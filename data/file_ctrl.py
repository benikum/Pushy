import sys
if __name__ == "__main__":
    sys.exit()

from PIL import Image
import os
import json

class JSONReadError(Exception):
    def __init__(self, msg="Cannot read JSON file"):
        self.msg = msg
        super().__init__(self.msg)

class JSONFileNotDict(Exception):
    def __init__(self, msg="JSON file is not a dictionary"):
        self.msg = msg
        super().__init__(self.msg)

class LevelImageTooBig(Exception):
    def __init__(self, msg="Image too big to compile"):
        self.msg = msg
        super().__init__(self.msg)

class IncorrectFileType(Exception):
    def __init__(self, msg="Image too big to compile"):
        self.msg = msg
        super().__init__(self.msg)

# reads a json file 
def json_read(file_path: str) -> dict:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        if file_path.split(".")[1] != "json":
            raise IncorrectFileType
        with open(file_path, "r") as file:
            json_data = json.load(file)
            if not isinstance(json_data, dict):
                raise JSONFileNotDict
            return json_data
    except (FileNotFoundError, IncorrectFileType, JSONFileNotDict) as e:
        raise JSONReadError(str(e))

def list_file_names(folder_path: str) -> list:
    file_names = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file_name)):
                file_names.append(file_name)
    return file_names

def get_tile_map(image_path: str) -> list:
    # loads rgb values from img into list
    image = Image.open(image_path)
    width, height = image.size
    total_pixels = width * height
    if total_pixels > 2500:
        raise LevelImageTooBig(str(total_pixels) + " pixels")
    rgb_map = list(image.getdata())
    
    # new empty level map
    level_map = [[] for _ in range(height)]
    color_keys = {}
    
    # every pixel in the image
    for i, pixel in enumerate(rgb_map):
        row = i // width
        
        # fill level_map with
        found_color = False
        for value, key in color_keys.items():
            # found existing color key
            if is_same_color(pixel, value):
                found_color = True
                level_map[row].append(key)
                break
        # add new color key
        if not found_color:
            new_key = chr(ord("A") + len(color_keys))
            color_keys[pixel] = new_key
            level_map[row].append(new_key)

    return level_map

def is_same_color(base_value: tuple, compare_value: tuple, tolerance = 16) -> bool:
    difference_value = max(abs(base_value[i] - compare_value[i]) for i in range(3))
    return (difference_value <= tolerance)

def save_tilemap(level_map: list, level_name = "new_level", overwrite = False):
    new_level_path = "assets/levels/" + level_name + ".json"
    
    if os.path.exists(new_level_path) or overwrite:
        raise FileExistsError("Level path already existing: " + new_level_path)
    
    map = [str.join(row) for row in level_map]
    
    width = len(level_map[0])
    height = len(level_map)
    
    # create json footprint
    level_layout = {}
    level_layout["name"] = level_name
    level_layout["width"] = width
    level_layout["height"] = height
    
    level_layout["level"] = {}
    level_layout["level"]["map"] = map
    level_layout["level"]["objects"] = [str(["-" for _ in range(width)]) for _ in range(height)]
    
    level_layout["level"]["materials"] = {}
    for key in list(set([item for item in row] for row in level_map)):
        level_layout["level"]["materials"][key] = "change_me"
    
    # save dict in json file
    with open(new_level_path, 'w') as file:
        json.dump(level_layout, file)

def compile_all_images():
    # check every filename in level dir for uncompiled png images
    for file in list_file_names("assets/levels"):
        name, extension = file.split(".")
        if extension == "png":
            try:
                raw_map = get_tile_map("assets/levels" + file), name
            except LevelImageTooBig as litb:
                print("Level image: " + file + " is too big! (" + str(litb) + "), maximum 2500")
                continue
            try:
                save_tilemap(raw_map, name)
            except FileExistsError:
                print("Cannot compile file: " + file + " because levelname already exists.")

class InstanceCache():
    # create new cache
    def __init__(self, class_type, *keys):
        self.class_type = class_type
        self.cache = {key:self.class_type(key) for key in keys if len(keys) > 0}
    # update existing key
    def change_key(self, key):
        self.cache[key] = self.class_type(key)
    # add a new key
    def add_key(self, key):
        if key not in list(self.cache.keys()):
            self.change_key(key)
    # use key and get value
    def load_key(self, key):
        self.add_key(key)
        return self.cache[key]

def repair_settings_file(incomplete_data: dict = {}) -> dict:
    default_data = {
        "language": "en",
        "resolution": [1280, 960],
        "fullscreen": False,
        "keybinds": {
            "move_up": "w",
            "move_down": "s",
            "move_left": "a",
            "move_right": "d",
            "game_restart": "r"
            }
        }
    
    settings_data = {}
    
    # compare default and incomplete data
    for key, value in default_data.items():
        if key in incomplete_data.keys():
            settings_data[key] = incomplete_data[key]
        else:
            settings_data[key] = value
    
    # save restored settings
    with open("settings.json", "w") as file:
        json.dump(settings_data, file, indent = 2)
        
    return settings_data