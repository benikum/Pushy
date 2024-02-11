import sys
if __name__ == "__main__":
    sys.exit()

from data.game import LevelMapController, Material

class PlayerController:
    def __init__(self, game_instance: LevelMapController):
        self.game_instance = game_instance
        self.texture = "pushy"
        self.orientation = 0
        self.load_player()
        
    def load_player(self):
        self.position = self.game_instance.start_pos
        self.game_instance.map[self.position[1]][self.position[0]].materials.append(Material("player"))
        
    def move(self, relative_position: tuple):
        self.position = self.game_instance.move_player(self.position, relative_position)
        
        if relative_position[1] < 0:
            self.orientation = 0
        elif relative_position[0] < 0:
            self.orientation = 1
        elif relative_position[1] > 0:
            self.orientation = 2
        elif relative_position[0] > 0:
            self.orientation = 3