import sys
if __name__ == "__main__":
    sys.exit()

import pygame

class GameScreenController:
    def __init__(self, game_instance, resolution, header_string = "Pushy Game"):
        self.game_instance = game_instance
        self.game_window = pygame.display.set_mode(resolution)

        self.block_size = resolution[0] // game_instance.board_width
        if self.block_size * game_instance.board_height > resolution[1]:
            self.block_size = resolution[1] // game_instance.board_height
        
        Texture.texture_size = self.block_size
        Texture.screen = self.game_window
        pygame.transform.scale(Texture.SHADE_OVERLAY, (self.block_size, self.block_size))

        pygame.display.set_caption(header_string)

        self.texture_cache = {}
        self.last_tick = 0
    def draw_screen(self):
        self.game_window.fill((0, 0, 0))
        for y in range(self.game_instance.board_height):
            for x in range(self.game_instance.board_width):
                texture_list = self.game_instance.map[y][x].get_textures()

                pos_x = x * self.block_size
                pos_y = y * self.block_size

                for i in texture_list:
                    if not i[0] in self.texture_cache:
                        self.texture_cache[i[0]] = Texture(i[0])
                    self.texture_cache[i[0]].draw_texture((pos_x, pos_y), i[1])
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

    SHADE_OVERLAY = pygame.Surface((1, 1), pygame.SRCALPHA)
    SHADE_OVERLAY.fill((0, 0, 0, 16))

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
