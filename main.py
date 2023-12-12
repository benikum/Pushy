import pygame
from pygame.locals import *
# import json
# import logging
import os
from data import json_control
from data import graphics
from data import game

def crashGame(errorCode):
    #programm beenden
    print("----CRASH----")
    print("Code" + str(errorCode))

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
        crashGame("files missing")

pygame.init()
clock = pygame.time.Clock()

# checkInstallation()
print("\n")

loaded_level = game.LevelMapController("level_1")
display = graphics.GameScreen(loaded_level)

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            break
        # if event.type == 
    # spielverlauf
    # grafik
    display.draw_screen()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()