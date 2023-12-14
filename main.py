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

level_map_controller = game.LevelMapController("level_1")
game_screen_controller = graphics.GameScreenController(level_map_controller, settings_json["resolution"])
player_controller = userinput.PlayerController(level_map_controller)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("bb :D")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_controller.move([0, -1])
            elif event.key == pygame.K_a:
                player_controller.move([-1, 0])
            elif event.key == pygame.K_s:
                player_controller.move([0, 1])
            elif event.key == pygame.K_d:
                player_controller.move([1, 0])
    game_screen_controller.draw_screen()
    clock.tick(10)