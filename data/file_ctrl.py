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
    return dict()

def list_file_names(folder_path):
    file_names = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file_name)):
                file_names.append(os.path.splitext(file_name)[0])
    return file_names