import json

def read(path):
    # path = path + filename + ".json"
    with open(path, "r") as file:
        json_data = json.load(file)
    return json_data

def write(path, content):
    pass