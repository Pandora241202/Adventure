import pygame
import os

class Object():
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
    
    def update_camera(self, scrollX, scrollY):
        self.rect.x += scrollX
        self.rect.y += scrollY

class Block(pygame.sprite.Sprite):
    
    WIDTH = 64
    HEIGHT = 64
    images = ['Soil.png', 'Grass Ground.png', 'Grass Left Rock Ground.png', 'Grass Right Rock Ground.png', 'Left Rock.png', 'Right Rock.png']
    
    def __init__(self, x, y, imgKind):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets\Map', self.images[imgKind-1]))
        self.image = pygame.transform.scale(self.image,(self.WIDTH, self.HEIGHT))
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT) 