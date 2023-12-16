from data import game

class PlayerController:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.position = self.game_instance.start_pos
        self.game_instance.map[self.position[1]][self.position[0]].addMaterial(game.PlayerEntity("green"))
    def move(self, relative_position):
        self.position = self.game_instance.moveEntity("player", self.position, relative_position)
        
        ori = 1 if relative_position[0] > 0 else 2 if relative_position[1] > 0 else 3 if relative_position[0] < 0 else 0
        self.game_instance.map[self.position[1]][self.position[0]].materials[-1].orientation = ori