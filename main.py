import pygame
from pygame.locals import *
# import json
import logging
import os
from data import json_control
# from data import graphics
# from data import player

def checkInstallation():
    necessary_files = [
        "assets",
        "assets/settings.json",
        "assets/language",
        "data",
        "data/game.py",
        "data/graphics.py",
        "data/json_control.py",
        "data/player.py",
        "data/textures.py"
    ]
    corrupt_files = []
    for file_path in necessary_files:
        found = os.path.exists(file_path)
        if not found:
            corrupt_files.append(file_path)
    print(str(len(corrupt_files)) + " Dateien fehlen")
    if len(corrupt_files) > 0:
        pygame.quit()

pygame.init()
# logging.base
# main_log = logging.getLogger(__main__)
checkInstallation()

settings_data = json_control.read("assets/settings.json")
window = pygame.display.set_mode(settings_data["resolution"])
pygame.display.set_caption("Pushy Game v.00001")

clock = pygame.time.Clock()

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            break
        # if event.type == 
    # spielverlauf
    # grafik
    pygame.display.flip()
    clock.tick(10)

pygame.quit()