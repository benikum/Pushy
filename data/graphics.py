import pygame
import random

class GameScreenController:
    def __init__(self, game_instance, resolution):
        self.game_instance = game_instance

        self.block_size = resolution[0] / game_instance.board_width
        # resolution[1] = self.block_size * game_instance.board_height

        self.game_window = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Pushy Game v.00001")

        self.materials = {}
    def draw_screen(self):
        self.game_window.fill((0, 0, 0))
        for h in range(self.game_instance.board_height):
            for w in range(self.game_instance.board_width):
                material = self.game_instance.map[h][w].texture
                if not material in self.materials:
                    self.materials[material] = Texture(material)
                pos_x = w * self.block_size
                pos_y = h * self.block_size
                # if self.materials[material].animated:
                #     self.materials[material].frame = random.choice(self.materials[material].frame_list)
                self.materials[material].blitTexture(self.game_window, (pos_x, pos_y), self.block_size)
                if self.game_instance.map[h][w].entity != None:
                    material = self.game_instance.map[h][w].entity.texture
                    if not material in self.materials:
                        self.materials[material] = Texture(material)
                    self.materials[material].blitTexture(self.game_window, (pos_x, pos_y), self.block_size)
        for t in list(self.materials.values()):
            t.nextFrame()
        pygame.display.flip()


class Texture:
    # error fallback img
    error_img = pygame.Surface((2, 2))
    error_img.fill((255, 0, 255))
    error_img.fill((0, 0, 0), rect=(1, 0, 1, 1))
    error_img.fill((0, 0, 0), rect=(0, 1, 1, 1))

    def __init__(self, texture_id):
        # load raw data
        self.texture_id = texture_id
        self.texture_path = "assets/textures/" + self.texture_id + ".png"
        self.img = self.loadTexture()
        self.rect = self.img.get_rect()
        self.size = self.rect.width
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        # check if the texture is animated
        self.isAnimated()
        # fill self.frame
        self.loadFrame()
    
    def loadTexture(self):
        # lädt png in self.img
        try:
            return pygame.image.load(self.texture_path)
        except:
            return self.error_img

    def isAnimated(self):
        # quadratisch (nicht animiert) / vielfaches lang (animiert)
        if self.rect.height == self.rect.width:
            self.animated = False
        elif self.rect.height % self.rect.width == 0:
            self.animated = True
        else:
            # cut away unusable frames
            self.img = self.img.subsurface(pygame.Rect(0, 0, self.rect.width, self.rect.width))
            # handle it as if it was square
            self.animated = False
    
    def loadFrame(self):
        # lädt self.frame aus self.img oder self.frame_list
        if self.animated:
            self.frame_list = []
            for y in range(0, self.rect.height, self.rect.width):
                frame_rect = pygame.Rect(0, y, self.rect.width, self.rect.width)
                frame_surface = self.img.subsurface(frame_rect)
                self.frame_list.append(frame_surface)
            self.frame_index = 0
            self.frame = self.frame_list[0]
        else:
            self.frame = self.img
    
    def nextFrame(self, reset = False):
        # wechselt zum nächsten frame
        if self.animated:
            if self.frame_index == len(self.frame_list) - 1 or reset:
                self.frame_index = 0
            else:
                self.frame_index += 1
            self.frame = self.frame_list[self.frame_index]
    
    
    def blitTexture(self, screen, position, size=32, rotation=0):
        rotation = (rotation % 4) * -90
        # blittet die texur
        self.frame = pygame.transform.scale(self.frame, (size, size))
        self.frame = pygame.transform.rotate(self.frame, rotation)
        # blittet die textur
        screen.blit(self.frame, position)