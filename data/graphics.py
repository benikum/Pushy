import sys
if __name__ == "__main__":
    sys.exit()

import pygame
from data.game import LevelMapController
from data.file_ctrl import InstanceCache
from data.userinput import PlayerController

class Texture:
    # fail img
    ERROR_IMG = pygame.Surface((2, 2))
    ERROR_IMG.fill((255, 0, 255))
    ERROR_IMG.fill((0, 0, 0), rect = (1, 0, 1, 1))
    ERROR_IMG.fill((0, 0, 0), rect = (0, 1, 1, 1))
    
    texture_size = 64
    
    def __init__(self, texture_id: str):
        # load raw data
        self.id = texture_id
        path = "assets/textures/" + self.id + ".png"
        try:
            self.img = pygame.image.load(path)
        except:
            print("Exception at loading texture: " + path)
            self.img = self.ERROR_IMG
        
        self.rect = self.img.get_rect()
        self.pos_x = self.rect.x
        self.animated = False
        
        self.compile_texture()

    def compile_texture(self):
        # square
        if self.rect.height == self.rect.width:
            self.img = pygame.transform.scale(self.img, (self.texture_size, self.texture_size))
            return
        # animated
        elif self.rect.height % self.rect.width == 0:
            self.animated = True
            self.frame_list = []
            # cut long picture
            for y in range(0, self.rect.height, self.rect.width):
                frame_rect = pygame.Rect(0, y, self.rect.width, self.rect.width)
                frame_surface = self.img.subsurface(frame_rect)
                frame_surface = pygame.transform.scale(frame_surface, (self.texture_size, self.texture_size))
                self.frame_list.append(frame_surface)
            self.frame_index = 0
            return
        # incorrect aspect ratio
        if self.rect.width < self.rect.height:
            self.img = self.img.subsurface(pygame.Rect(0, 0, self.rect.width, self.rect.width))
        else:
            self.img = self.img.subsurface(pygame.Rect(0, 0, self.rect.height, self.rect.height))
    
    def load_frame(self):
        # lädt self.frame aus self.img oder self.frame_list
        if self.animated:
            self.frame =  self.frame_list[self.frame_index]
        else:
            self.frame =  self.img
    
    def set_frame_rotation(self, rot: int):
        self.frame = pygame.transform.rotate(self.frame, rot)
    
    def next_frame(self):
        # wechselt zum nächsten frame
        if not self.animated:
            return
        elif self.frame_index == len(self.frame_list) - 1 :
            self.frame_index = 0
        else:
            self.frame_index += 1
    
    def draw_frame(self, position: tuple):
        self.screen.blit(self.frame, position)

class GameScreenController:
    texture_cache = InstanceCache(Texture)
    def __init__(self, game_instance: LevelMapController, player_instance: PlayerController, resolution: tuple, fullscreen: bool, window_caption = "Pushy Game"):
        self.game_instance = game_instance
        self.player_instance = player_instance
        self.game_window = pygame.display.set_mode(resolution)
        
        # calculate block size
        self.block_size = resolution[0] // game_instance.map_width
        if self.block_size * game_instance.map_height > resolution[1]:
            self.block_size = resolution[1] // game_instance.map_height
        
        # move blocks into middle
        self.x_offset = (resolution[0] - (game_instance.map_width * self.block_size)) // 2
        self.y_offset = (resolution[1] - (game_instance.map_height * self.block_size)) // 2
        
        Texture.texture_size = self.block_size
        Texture.ERROR_IMG = pygame.transform.scale(Texture.ERROR_IMG, (Texture.texture_size, Texture.texture_size))
        Texture.screen = self.game_window
        pygame.display.set_caption(window_caption)
        
        self.last_tick = 0
    
    def draw_frame(self):
        self.game_window.fill((0, 0, 0))
        for y in range(self.game_instance.map_height):
            for x in range(self.game_instance.map_width):
                texture_list = self.game_instance.map[y][x].get_textures()

                pos_x = x * self.block_size + self.x_offset
                pos_y = y * self.block_size + self.y_offset

                for texture in texture_list:
                    current_texture = self.texture_cache.load_key(texture)
                    current_texture.load_frame()
                    current_texture.draw_frame((pos_x, pos_y))
        
        player_texture = self.texture_cache.load_key(self.player_instance.texture)
        player_texture.load_frame()
        player_texture.set_frame_rotation(self.player_instance.orientation * 90)
        pos_x, pos_y = self.player_instance.position
        pos_x *= self.block_size + self.x_offset
        pos_y *= self.block_size + self.y_offset
        player_texture.draw_frame((pos_x, pos_y))
        
        # if enough time has passed, every texture instance gets a new frame
        new_tick = pygame.time.get_ticks()
        if new_tick - self.last_tick >= 80:
            for texture in list(self.texture_cache.cache.values()):
                texture.next_frame()
            self.last_tick = new_tick
        
        # display frame on screen window
        pygame.display.flip()