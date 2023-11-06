import pygame
import os

class Object(pygame.sprite.Sprite):
    pass

class Block(pygame.sprite.Sprite):
    
    WIDTH = 64
    HEIGHT = 64
    images = {'Soil', 'Grass Ground', 'Grass Left Rock Ground', 'Grass Right Rock Ground', 'Left Rock', 'Right Rock'}
    
    def __init__(self, x, y, imgKind):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets\Map', self.image[imgKind]))
        self.image = pygame.transform.scale(self.image,(self.WIDTH, self.HEIGHT))
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT) 