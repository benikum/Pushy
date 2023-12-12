import pygame
from pygame.locals import *
# import json
# import logging
import os
import sys
from data import json_control
from data import graphics
from data import game

def checkInstallation():
    necessary_files = [
        "assets",
        "assets/settings.json",
        "assets/lang",
        "assets/levels",
        "assets/materials",
        "assets/textures",
        "data",
        "data/game.py",
        "data/graphics.py",
        "data/json_control.py",
        "data/player.py"
    ]
    corrupt_files = []
    for file_path in necessary_files:
        found = os.path.exists(file_path)
        if not found:
            corrupt_files.append(file_path)
    print(str(len(corrupt_files)) + " files missing")
    if len(corrupt_files) > 0:
        print("SHUTTING DOWN")
        sys.exit()
checkInstallation()

pygame.init()
clock = pygame.time.Clock()

settings_json = json_control.read("assets/settings.json")

loaded_level = game.LevelMapController("level_1")
display = graphics.GameScreen(loaded_level, settings_json["resolution"])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("bb :D")
            pygame.quit()
            sys.exit()
    display.draw_screen()
    clock.tick(10)