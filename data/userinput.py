from data import game

class PlayerController:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.position = self.game_instance.start_pos
        self.game_instance.map[self.position[1]][self.position[0]].addMaterial(game.PlayerEntity)
    def move(self, relative_position):
        new_pos_x = self.position[0] + relative_position[0]
        new_pos_y = self.position[1] + relative_position[1]
        self.position = self.game_instance.moveEntity(self.position, [new_pos_x, new_pos_y])