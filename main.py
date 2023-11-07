import pygame
import os
from player import Player
from enemy import Enemy
from cannon import Cannon
from object import Block
from mapobjects import MapObjects

pygame.init()

SCENE_NAME_AREA = (0, 0)
BLOCK_SIZE = 64
FONT = pygame.font.Font('freesansbold.ttf', 32)
FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640
SCROLL_THRESHOLD_X = 768
SCROLL_THRESHOLD_Y = 300

pygame.display.set_caption('Adventure Of Zero')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
class Scene():
    def __init__(self):
        self.nextscene = self
    
    def next_scene(self):
        raise NotImplementedError
    
    def update(self, inputs):
        raise NotImplementedError
    
    def render(self, screen):
        raise NotImplementedError
    
    def terminate(self):
        self.nextscene = None
    
class MenuScene(Scene):
    def __init__(self):
        super().__init__()
    
    def next_scene(self):
        return PlayScene()

    def update(self, inputs):
        pass
    
    def render(self):
        screen.fill((0, 0, 0))
        scene_name = FONT.render('Menu Scene', True, (255, 255, 255))
        screen.blit(scene_name, SCENE_NAME_AREA)
class EndScene(Scene):
    def __init__(self):
        super().__init__()
    
    def next_scene(self):
        return MenuScene()

    def update(self, inputs):
        pass
    
    def render(self):
        screen.fill((0, 0, 0))
        scene_name = FONT.render('End Scene', True, (255, 255, 255))
        screen.blit(scene_name, SCENE_NAME_AREA)

############ PLAY SCENE ############

class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        
        # Player
        self.playerGroup = pygame.sprite.Group()
        player = Player(0, SCREEN_HEIGHT - BLOCK_SIZE*3 - Player.HEIGHT + Player.BOTTOM_SPACE)
        self.playerGroup.add(player)
        
        # Enemy
        self.enemyGroup = pygame.sprite.Group()
        enemy = Enemy(BLOCK_SIZE*3, SCREEN_HEIGHT - BLOCK_SIZE*3 - Enemy.HEIGHT + Enemy.BOTTOM_SPACE, BLOCK_SIZE*2, (SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE)
        self.enemyGroup.add(enemy)
        
        # Cannon
        self.cannonGroup = pygame.sprite.Group()
        cannon = Cannon(0, SCREEN_HEIGHT - 2 * BLOCK_SIZE - Cannon.HEIGHT + Cannon.BOTTOM_SPACE, True)
        self.cannonGroup.add(cannon)
        cannon = Cannon((SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE, SCREEN_HEIGHT - 2 * BLOCK_SIZE - Cannon.HEIGHT + Cannon.BOTTOM_SPACE, False)
        self.cannonGroup.add(cannon)
        
        # Map Objects
        self.mapObjects = MapObjects(
            [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,3,2,1,2,4,0,0,3,4,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,3,2,1,1,1,1,1,2,2,1,6,0,0,1,0,0,0,3,2,2,2,2,2,2,2,2,2,4,0,0,2],
             [3,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,6,0,0,1,0,0,0,5,1,1,1,1,1,1,1,1,1,6,0,0,1],
             [5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,0,0,1,0,0,0,5,1,1,1,1,1,1,1,1,1,6,0,0,1],
             [5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,0,0,1,0,0,0,5,1,1,1,1,1,1,1,1,1,6,0,0,1],
             [5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,0,0,1,0,0,0,5,1,1,1,1,1,1,1,1,1,6,0,0,1],]
        )
        
        # Scroll map
        self.cameraX = SCREEN_WIDTH - SCROLL_THRESHOLD_X
        self.cameraY = SCREEN_HEIGHT - SCROLL_THRESHOLD_Y
            
    def next_scene(self):
        return EndScene()

    def update(self, inputs):
        (scrollX , scrollY) = (0, 0)
        (scrollX, scrollY) = self.playerGroup.sprites()[0].update(inputs, self.mapObjects.blockGroup.sprites())
        self.enemyGroup.update(self.playerGroup.sprites()[0], scrollX, scrollY)
        self.cannonGroup.update(self.playerGroup.sprites()[0])
        for cannon in self.cannonGroup.sprites():
            cannon.cannonBallGroup.update(self.playerGroup.sprites()[0])       
        self.mapObjects.update(scrollX, scrollY)
    
    def render(self):
        screen.fill((255, 255, 255))
        # Draw map scene
        self.mapObjects.draw(screen)
        # Draw the player 
        self.playerGroup.draw(screen)
        # Draw enemy
        self.enemyGroup.draw(screen)
        # self.cannonGroup.draw(screen)
        # for cannon in self.cannonGroup.sprites():
        #     cannon.cannonBallGroup.draw(screen)

        scene_name = FONT.render('Play Scene', True, (0, 0, 0))
        screen.blit(scene_name, SCENE_NAME_AREA)
    
class Game():
    def __init__(self):
        self.active_scene = MenuScene()
    
    def run(self):
        while self.active_scene != None:
            pressed_keys = pygame.key.get_pressed()
            # filtered_events = []
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active_scene.terminate()
                else:
                    # TAB to next scene
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        self.active_scene = self.active_scene.next_scene()
                # filtered_events.append(event)
            
            # Manage scene
            input_keys = pygame.key.get_pressed()
            self.active_scene.update(input_keys)
            self.active_scene.render()
            
            self.active_scene = self.active_scene.nextscene
            
            # Update and tick
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    clock = pygame.time.Clock()
    game = Game()
    game.run()
    pygame.quit()
    
# Ref https://github.com/joncoop/pygame-scene-manager/blob/master/scene_manager.py