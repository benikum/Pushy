import pygame

class Texture:
    # error fallback img
    error_img = pygame.Surface((2, 2))
    error_img.fill((255, 0, 255))
    error_img.fill((0, 0, 0), rect=(1, 0, 1, 1))
    error_img.fill((0, 0, 0), rect=(0, 1, 1, 1))

    def __init__(self, path):
        self.path = path
        self.img = self.loadTexture()
        self.rect = self.img.get_rect()

        self.size = self.rect.width
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        self.animated = self.isAnimated()

        self.loadFrame
    
    def setSize(self, size):
        # setzt blit size (quadratisch) / ansonsten wie png width
        self.size = size
    
    def setPos(self, x, y):
        # setzt blit position
        self.pos_x = x
        self.pos_y = y
    
    def loadTexture(self):
        # lädt png in self.img
        try:
            return pygame.image.load(self.path)
        except:
            return error_img

    def isAnimated(self):
        # quadratisch (nicht animiert) / vielfaches lang (animiert)
        if self.rect.height == self.rect.width:
            return False
        if self.rect.height % self.rect.width == 0:
            return True
        self.img = self.img.subsurface(pygame.Rect(0, 0, self.rect.width, self.rect.width))
        return False
    
    def loadFrame(self):
        # lädt self.frame aus self.img oder self.frame_list
        if self.animated:
            self.frame_list = []
            for y in range(0, self.rect.height, self.rect.width):
                frame_rect = pygame.Rect(0, y, self.rect.width, self.rect.height)
                frame_surface = self.img.subsurface(frame_rect)
                pygame.transform.scale(frame_surface, (self.size, self.size))
                self.frame_list.append(frame_surface)
            self.frame_index = 0
            self.frame = self.frame_list[0]
        else:
            self.frame = self.img
            pygame.transform.scale(self.frame, (self.size, self.size))
    
    def nextFrame(self, reset = False):
        # wechselt zum nächsten frame
        if self.animated:
            if self.frame_index == len(self.frame) - 1 or reset:
                self.frame_index = 0
            else:
                self.frame_index += 1
            self.frame = self.frame_list[self.frame_index]
    
    def blit(self, screen):
        # blittet die textur
        screen.blit(self.frame, (self.pos_x, self.pos_y))