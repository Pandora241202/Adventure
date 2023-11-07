import pygame
from object import Block

class MapObjects():
    
    WIDTH = 1280
    HEIGHT = 640
    SCROLL_THRESHOLD_X = 768
    SCROLL_THRESHOLD_Y = 300
    SCREEN_COUNT = 2
    
    def __init__(self, map):
        self.blockGroup = pygame.sprite.Group()          
        
        for i in range(len(map)):
            for j in range(len(map[i])):
                if (map[i][j]) != 0:
                    self.blockGroup.add(Block(j*Block.WIDTH, i*Block.HEIGHT, map[i][j]))
    
    def update(self, scrollX, scrollY):
        # Scroll
        for o in self.blockGroup.sprites():
            o.rect.x += scrollX
            o.rect.y += scrollY
        
    def draw(self, screen):
        self.blockGroup.draw(screen)