import pygame
from pygame.locals import *
# import json
# import logging
import os
import sys
from data import json_control
from data import game
from data import graphics
from data import userinput

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
        "data/userinput.py"
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

level = game.LevelMapController("level_1")
display = graphics.GameScreenController(level, settings_json["resolution"])
playerC = userinput.PlayerController(level)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("bb :D")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                playerC.move([0, -1])
            elif event.key == pygame.K_a:
                playerC.move([-1, 0])
            elif event.key == pygame.K_s:
                playerC.move([0, 1])
            elif event.key == pygame.K_d:
                playerC.move([1, 0])
    display.draw_screen()
    clock.tick(10)