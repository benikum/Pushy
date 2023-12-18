import sys
if __name__ == "__main__":
    sys.exit()

import pygame

class GameScreenController:
    def __init__(self, game_instance, resolution, header_string = "Pushy Game"):
        self.game_instance = game_instance

        block_size = resolution[0] / game_instance.board_width
        if block_size * game_instance.board_height > resolution[1]:
            block_size = resolution[1] / game_instance.board_height
        self.block_size = int(block_size)

        self.game_window = pygame.display.set_mode(resolution)
        pygame.display.set_caption(header_string)

        self.materials = dict()
    def draw_screen(self):
        self.game_window.fill((0, 0, 0))
        for y in range(self.game_instance.board_height):
            for x in range(self.game_instance.board_width):
                tile = self.game_instance.map[y][x]
                pos_x = x * self.block_size
                pos_y = y * self.block_size

                texture_list = tile.get_textures()
                layer_height = tile.get_entity_attributes()[2]
                for i in texture_list:
                    if not i[0] in self.materials:
                        self.materials[i[0]] = Texture(i[0])
                    self.materials[i[0]].blitTexture(self.game_window, (pos_x, pos_y), self.block_size, i[1])
        for t in list(self.materials.values()):
            t.next_frame()
        pygame.display.flip()

class Texture:
    # error fallback img
    ERROR_IMG = pygame.Surface((2, 2))
    ERROR_IMG.fill((255, 0, 255))
    ERROR_IMG.fill((0, 0, 0), rect=(1, 0, 1, 1))
    ERROR_IMG.fill((0, 0, 0), rect=(0, 1, 1, 1))

    def __init__(self, texture_id):
        # load raw data
        self.texture_id = texture_id
        self.texture_path = "assets/textures/" + self.texture_id + ".png"
        self.img = self.load_texture()
        self.rect = self.img.get_rect()
        self.size = self.rect.width
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        # check if the texture is animated
        self.is_animated()
        # fill self.frame
    
    def load_texture(self):
        # lädt png in self.img
        try:
            return pygame.image.load(self.texture_path)
        except:
            return self.ERROR_IMG

    def is_animated(self):
        # quadratisch (nicht animiert) / vielfaches lang (animiert)
        if self.rect.height == self.rect.width:
            self.animated = False
        elif self.rect.height % self.rect.width == 0:
            self.animated = True
            self.frame_list = []
            for y in range(0, self.rect.height, self.rect.width):
                frame_rect = pygame.Rect(0, y, self.rect.width, self.rect.width)
                frame_surface = self.img.subsurface(frame_rect)
                self.frame_list.append(frame_surface)
            self.frame_index = 0
        else:
            # cut away unusable frames
            self.img = self.img.subsurface(pygame.Rect(0, 0, self.rect.width, self.rect.width))
            # handle it as if it was square
            self.animated = False
    
    def load_frame(self):
        # lädt self.frame aus self.img oder self.frame_list
        if self.animated:
            self.frame = self.frame_list[self.frame_index if self.animated else 0]
        else:
            self.frame = self.img
    
    def next_frame(self, reset = False):
        # wechselt zum nächsten frame
        if not self.animated:
            return 0
        if self.frame_index == len(self.frame_list) - 1 or reset:
            self.frame_index = 0
        else:
            self.frame_index += 1
    
    def blitTexture(self, screen, position, size=32, rotation=0):
        rotation = (rotation % 4) * -90
        # blittet die texur
        self.load_frame()
        self.frame = pygame.transform.scale(self.frame, (size, size))
        self.frame = pygame.transform.rotate(self.frame, rotation)
        # blittet die textur
        screen.blit(self.frame, position)