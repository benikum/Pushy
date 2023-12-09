import pygame
from pygame.locals import *

pygame.init()

class AnimatedImage:
    def __init__(self, x, y, texture_path):
        self.x = x
        self.y = y
        self.frames = self.load_frames(texture_path)
        self.num_frames = len(self.frames)
        self.frame_index = 0
        self.overlay_color = (0, 0, 255, 128)  # Blaues Overlay mit 50% Transparenz

    def load_frames(self, texture_path):
        frames = []
        try:
            texture = pygame.image.load(texture_path)
            frame_width = texture.get_width() // texture.get_height()
            frame_height = texture.get_height()
            for i in range(frame_width):
                frame = pygame.Surface((frame_height, frame_height), pygame.SRCALPHA)
                frame.blit(texture, (0, 0), (i * frame_height, 0, frame_height, frame_height))
                frames.append(frame)
        except pygame.error:
            print(f"Warnung: Textur {texture_path} nicht gefunden. Verwende Ausweichtextur.")
            return [pygame.Surface((32, 32))]  # Platzhalter-Ausweichtextur

        return frames

    def draw(self, surface):
        surface.blit(self.frames[self.frame_index], (self.x, self.y))
        pygame.draw.rect(surface, self.overlay_color, (self.x, self.y, self.frames[0].get_width(), self.frames[0].get_height()))

    def update_animation(self):
        self.frame_index = (self.frame_index + 1) % self.num_frames

width, height = 800, 600
window = pygame.display.set_mode(size=(width, height))
pygame.display.set_caption("Animierte Textur mit Overlay")

clock = pygame.time.Clock()

# Lade animierte Textur
texture_path = "img/water_still.png"
animated_texture = AnimatedImage(100, 100, texture_path)

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            break

    window.fill((255, 255, 255))  # Weißer Hintergrund

    # Blitte die animierte Textur und füge das Overlay hinzu
    animated_texture.draw(window)
    animated_texture.update_animation()

    pygame.display.update()
    clock.tick(10)  # Geschwindigkeit der Animation

pygame.quit()
