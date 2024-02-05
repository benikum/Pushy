import sys
if __name__ == "__main__":
    sys.exit()

import pygame
from data.game import LevelMapController

class GameScreenController:
    texture_cache = {}
    def __init__(self, game_instance: LevelMapController, resolution: tuple, window_caption: str = "Pushy Game"):
        self.game_instance = game_instance
        self.game_window = pygame.display.set_mode(resolution)
        
        self.block_size = resolution[0] // game_instance.map_width
        if self.block_size * game_instance.map_height > resolution[1]:
            self.block_size = resolution[1] // game_instance.map_height
        
        self.x_offset = resolution[0] - (game_instance.map_width * self.block_size) // 2
        self.y_offset = resolution[1] - (game_instance.map_height * self.block_size) // 2
        
        Texture.texture_size = self.block_size
        Texture.screen = self.game_window
        pygame.display.set_caption(window_caption)
        
        self.last_tick = 0
    
    def load_texture(self, texture_id: str):
        self.texture_cache[texture_id] = Texture(texture_id)
    
    def draw_screen(self):
        self.game_window.fill((0, 0, 0))
        for y in range(self.game_instance.map_height):
            for x in range(self.game_instance.map_width):
                texture_list = self.game_instance.map[y][x].get_textures()

                pos_x = x * self.block_size + self.x_offset
                pos_y = y * self.block_size + self.y_offset

                for texture in texture_list:
                    self.texture_cache[texture[0]].draw_texture((pos_x, pos_y), texture[1])
        
        # FIXME
        for t in list(self.texture_cache.values()):
            new_tick = pygame.time.get_ticks()
            if new_tick - self.last_tick >= 80:
                t.next_frame()
                self.last_tick = new_tick
        pygame.display.flip()

class Texture:
    # error fallback img
    ERROR_IMG = pygame.Surface((2, 2))
    ERROR_IMG.fill((255, 0, 255))
    ERROR_IMG.fill((0, 0, 0), rect=(1, 0, 1, 1))
    ERROR_IMG.fill((0, 0, 0), rect=(0, 1, 1, 1))

    screen = None
    texture_size = None

    def __init__(self, texture_id):
        # load raw data
        self.texture_id = texture_id
        self.texture_path = "assets/textures/" + self.texture_id + ".png"
        self.img = self.load_texture()
        self.rect = self.img.get_rect()
        self.size = self.rect.width
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.shade = 0
        # check if the texture is animated
        self.is_animated()
    
    def load_texture(self):
        # lädt png in self.img
        try:
            return pygame.image.load(self.texture_path)
        except:
            return self.ERROR_IMG

    def is_animated(self):
        # quadratisch (nicht animiert) / vielfaches lang (animiert)
        if not self.rect.height == self.rect.width:
            if self.rect.height % self.rect.width == 0:
                self.animated = True
                self.frame_list = []
                for y in range(0, self.rect.height, self.rect.width):
                    frame_rect = pygame.Rect(0, y, self.rect.width, self.rect.width)
                    frame_surface = self.img.subsurface(frame_rect)
                    frame_surface = pygame.transform.scale(frame_surface, (self.texture_size, self.texture_size))
                    self.frame_list.append(frame_surface)
                self.frame_index = 0
                return
            self.img = self.img.subsurface(pygame.Rect(0, 0, self.rect.width, self.rect.width))
        self.animated = False
        self.img = pygame.transform.scale(self.img, (self.texture_size, self.texture_size))
    
    def load_frame(self):
        # lädt self.frame aus self.img oder self.frame_list
        if self.animated:
            self.frame = self.frame_list[self.frame_index]
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
    
    def draw_texture(self, position, rotation=0):
        self.load_frame()
        self.frame = pygame.transform.rotate(self.frame, (rotation % 4) * -90)
        self.screen.blit(self.frame, position)
