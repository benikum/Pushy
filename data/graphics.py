import pygame

class GameScreen:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.materials = [m in self.game_instance.json_data["tile_map"]["materials"].values()]
        self.

class Texture:
    # error fallback img
    error_img = pygame.Surface((2, 2))
    error_img.fill((255, 0, 255))
    error_img.fill((0, 0, 0), rect=(1, 0, 1, 1))
    error_img.fill((0, 0, 0), rect=(0, 1, 1, 1))

    def __init__(self, path):
        # load raw data
        self.path = path
        self.img = self.loadTexture()
        self.rect = self.img.get_rect()
        self.size = self.rect.width
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        # check if the texture is animated
        self.isAnimated()
        # fill self.frame
        self.loadFrame
    
    def loadTexture(self):
        # lädt png in self.img
        try:
            return pygame.image.load(self.path)
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
                frame_rect = pygame.Rect(0, y, self.rect.width, self.rect.height)
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
    
    def setSize(self, size):
        # setzt blit size (quadratisch) / ansonsten wie png width
        self.size = size
    
    def setPosition(self, x, y):
        # setzt blit position
        self.pos_x = x
        self.pos_y = y
    
    def setRotation(self, rotation_side):
        #  0
        # 3 1
        #  2
        self.rotation = (rotation_side % 4) * -90
    
    def blit(self, screen):
        # blittet die texur
        self.loadFrame()
        self.frame = pygame.transform.scale(self.frame, (self.size, self.size))
        self.frame = pygame.transform.rotate(self.frame, self.rotation)
        # blittet die textur
        screen.blit(self.frame, (self.pos_x, self.pos_y))

def newFrame(map_instance):
    screen.fill((255, 255, 255))
    
    pygame.display.flip()