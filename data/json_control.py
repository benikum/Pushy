import json

def read(path):
    try:
        with open(path, "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        json_data = {}
    return json_data

def write(path, content):
    pass