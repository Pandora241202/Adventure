import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.name = name
        self.width = width
        self.height = height
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.image.fill((0, 100, 50))
        self.name = 'block'
        self.mask = pygame.mask.from_surface(self.image)