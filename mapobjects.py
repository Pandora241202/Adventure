import pygame
from object import Block

class MapObjects():
    
    WIDTH = 1280
    HEIGHT = 640
    SCROLL_THRESHOLD_X = 1088
    SCROLL_THRESHOLD_Y = 256
    SCREEN_COUNT = 2
    
    def __init__(self, map):
        self.blockGroup = pygame.sprite.Group()          
        
        for i in range(len(map)):
            for j in range(len(map[i])):
                if (map[i][j]) == 1:
                    self.blockGroup.add(Block(j*self.BLOCK_SIZE, i*self.BLOCK_SIZE, map[i][j]))
    
    def update(self, scrollX, scrollY):
        # Scroll
        for o in self.blockGroup.sprites():
            o.rect.x += scrollX
            o.rect.y += scrollY
        
    def draw(self, screen):
        self.blockGroup.draw(screen)