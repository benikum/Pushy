class PlayerController:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        # self.color
        self.position = self.game_instance.start_pos
    def move(self, relative_position):
        new_pos_x = self.position[0] + relative_position[0]
        new_pos_y = self.position[1] + relative_position[1]
        if 0 <= new_pos_x <= self.game_instance.board_width and 0 <= new_pos_y <= self.game_instance.board_height:
            self.position = self.game_instance.moveEntity(self.position, [new_pos_x, new_pos_y])