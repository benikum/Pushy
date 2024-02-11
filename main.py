import os
import sys

NECESSARY_FILES = [
    "assets",
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

import pygame
from data.game import LevelMapController
from data.graphics import GameScreenController
from data.userinput import PlayerController
from data.file_ctrl import JSONReadError, json_read, list_file_names, compile_all_images, repair_settings_file

class JSONDataIncomplete(Exception):
    def __init__(self, msg="JSON file has missing "):
        self.msg = msg
        super().__init__(self.msg)

# load settings data
try:
    raw_settings_data = json_read("settings.json")
except JSONReadError as jsonre:
    print("Exception while loading settings.json" + str(jsonre))
    raw_settings_data = {}
SETTINGS_DATA = repair_settings_file(raw_settings_data)
KEYBINDS = SETTINGS_DATA["keybinds"]

LEVEL_LIST = [os.path.splitext(file)[0] for file in list_file_names("assets/levels")]
if len(LEVEL_LIST) == 0:
    print("no levels")
    sys.exit()
compile_all_images()

current_level_index = 0

def load_level(level_id: str = LEVEL_LIST[current_level_index]):
    global current_level_index, level_map_controller, game_screen_controller, player_controller
    
    level_map_controller = LevelMapController(level_id)
    player_controller = PlayerController(level_map_controller)
    game_screen_controller = GameScreenController(level_map_controller, player_controller, SETTINGS_DATA.get("resolution", [800, 600]), False, level_map_controller.level_name)

def next_level():
    global current_level_index
    
    current_level_index = current_level_index + 1 if not current_level_index == len(LEVEL_LIST) -1 else 0
    load_level()


pygame.init()
# clock = pygame.time.Clock()

load_level()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT \
        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == getattr(pygame, "K_" + KEYBINDS.get("move_up", "w")):
                player_controller.move((0, -1))
            elif event.key == getattr(pygame, "K_" + KEYBINDS.get("move_left", "a")):
                player_controller.move((-1, 0))
            elif event.key == getattr(pygame, "K_" + KEYBINDS.get("move_down", "s")):
                player_controller.move((0, 1))
            elif event.key == getattr(pygame, "K_" + KEYBINDS.get("move_right", "d")):
                player_controller.move((1, 0))
            elif event.key == getattr(pygame, "K_" + KEYBINDS.get("game_restart", "r")):
                load_level()
    for event in level_map_controller.game_events:
        if event == "win":
            next_level()
    game_screen_controller.draw_frame()
    pygame.time.Clock().tick(60)
    # clock.tick(60)