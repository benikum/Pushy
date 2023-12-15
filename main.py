import pygame
# from pygame.locals import *
import os
import sys
import json
from data.game import LevelMapController
from data.graphics import GameScreenController
from data.userinput import PlayerController

# check if all files are there
necessary_files = [
    "assets",
    "assets/settings.json",
    "assets/lang",
    "assets/levels",
    "assets/materials",
    "assets/textures",
]
corrupt_files = []
for file_path in necessary_files:
    found = os.path.exists(file_path)
    if not found:
        corrupt_files.append(file_path)
if len(corrupt_files) > 0:
    sys.exit()

pygame.init()
clock = pygame.time.Clock()

with open("assets/settings.json", "r") as file:
    settings_json = json.load(file)

def loadLevel(level_id):
    global level_map_controller, game_screen_controller, player_controller
    
    level_map_controller = LevelMapController(level_id)
    game_screen_controller = GameScreenController(level_map_controller, settings_json["resolution"])
    player_controller = PlayerController(level_map_controller)

loadLevel("level_1")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player_controller.move([0, -1])
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player_controller.move([-1, 0])
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player_controller.move([0, 1])
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player_controller.move([1, 0])
            elif event.key == pygame.K_r:
                loadLevel(level_map_controller.map_id)
    game_screen_controller.draw_screen()
    clock.tick(10)