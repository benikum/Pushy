from json import load
import pygame
import os
import sys
from data.game import LevelMapController
from data.graphics import GameScreenController
from data.userinput import PlayerController
from data.file_ctrl import json_read, list_file_names

# check if all files are there
NECESSARY_FILES = [
    "assets",
    "assets/settings.json",
    "assets/lang",
    "assets/levels",
    "assets/materials",
    "assets/textures",
    "data",
    "data/file_ctrl.py",
    "data/game.py",
    "data/graphics.py",
    "data/userinput.py"]
corrupt_files = [file_path for file_path in NECESSARY_FILES if not os.path.exists(file_path)]
if len(corrupt_files) > 0:
    print("missing files: ", corrupt_files)
    sys.exit()

pygame.init()
clock = pygame.time.Clock()

settings_json = json_read("assets/settings.json")
key_list = {"w":pygame.K_w,"a":pygame.K_a,"s":pygame.K_s,"d":pygame.K_d,"r":pygame.K_r}

level_list = list_file_names("assets/levels")
if len(level_list) == 0:
    sys.exit()
loaded_level = 0

def next_level():
    global loaded_level
    
    loaded_level = loaded_level + 1 if (not loaded_level == len(level_list) - 1) else 0
    load_level(level_list[loaded_level])
    
def load_level(level_id):
    global level_map_controller, game_screen_controller, player_controller
    
    level_map_controller = LevelMapController(level_id)
    game_screen_controller = GameScreenController(level_map_controller, settings_json.get("resolution", [600, 800]), level_map_controller.level_name)
    player_controller = PlayerController(level_map_controller)

load_level(level_list[loaded_level])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == key_list.get(settings_json.get("move_up", "w"), pygame.K_w):
                player_controller.move([0, -1])
            elif event.key == key_list.get(settings_json.get("move_left", "a"), pygame.K_a):
                player_controller.move([-1, 0])
            elif event.key == key_list.get(settings_json.get("move_down", "s"), pygame.K_s):
                player_controller.move([0, 1])
            elif event.key == key_list.get(settings_json.get("move_right", "d"), pygame.K_d):
                player_controller.move([1, 0])
            elif event.key == key_list.get(settings_json.get("game_restart", "r"), pygame.K_r):
                load_level(level_map_controller.map_id)
    for event in level_map_controller.event_listener():
        if event == "win":
            next_level()
    game_screen_controller.draw_screen()
    clock.tick(10)