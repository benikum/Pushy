from PIL import Image
import os
import json

def json_read(file_path):
    if isinstance(file_path, str) and os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
                if isinstance(json_data, dict):
                    return json_data
        except Exception as error:
            print("Unexpected Error: " + str(error))
    return {}

def list_file_names(folder_path):
    file_names = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file_name)):
                file_names.append(file_name)
    return file_names

def get_tile_map(image_path, tolerance=16):
    image = Image.open(image_path)
    width, height = image.size
    rgb_map = list(image.getdata())
    
    level_map = [[] for _ in range(height)]
    color_map = {}

    for i, pixel in enumerate(rgb_map):
        row = i // width

        found_color = False
        for value, key in color_map.items():
            if is_same_color(pixel, value, tolerance):
                found_color = True
                level_map[row].append(key)
                break

        if not found_color:
            new_key = chr(ord("A") + len(color_map))
            color_map[pixel] = new_key
            level_map[row].append(new_key)

    return level_map

def is_same_color(base_value, compare_value, tolerance=16):
    difference_value = max(abs(base_value[i] - compare_value[i]) for i in range(3))
    return difference_value <= tolerance

def save_tilemap(level_map, level_name = "new_level"):
    new_level_path = "assets/levels/" + level_name + ".json"
    if os.path.exists(new_level_path):
        return False

    tile_map = [str().join(row) for row in level_map]

    level_layout = {}
    level_layout["start"] = [0, 0]
    level_layout["finish"] = [0, 0]
    level_layout["entities"] = []

    level_layout["name"] = level_name
    level_layout["width"] = len(level_map[0])
    level_layout["height"] = len(level_map)
    level_layout["tile_map"] = {}
    level_layout["tile_map"]["map"] = tile_map
    print(level_layout)

    with open(new_level_path, 'w') as new_file:
        json.dump(level_layout, new_file)
    return True

def compile_all_images():
    for file in list_file_names("assets"):
        name, extension = file.split(".")
        if extension == "png":
            save_tilemap(get_tile_map("assets/levels" + file), name)