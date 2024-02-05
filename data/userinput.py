import sys
if __name__ == "__main__":
    sys.exit()

from data.game import LevelMapController, Material

class PlayerController:
    def __init__(self, game_instance: LevelMapController):
        self.game_instance = game_instance
        self.position = self.game_instance.start_pos #TODO
        self.game_instance.map[self.position[1]][self.position[0]].materials.append(Material("player"))
    def move(self, relative_position):
        self.position = self.game_instance.move_entity("player", self.position, relative_position)
        
        ori = 1 if relative_position[0] > 0 else 2 if relative_position[1] > 0 else 3 if relative_position[0] < 0 else 0
        self.game_instance.map[self.position[1]][self.position[0]].materials[-1].orientation = ori