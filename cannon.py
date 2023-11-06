import pygame
import os
from object import Object

class AnimInfo():
   def __init__(self, startFrame, numFrames):
       self.startFrame = startFrame
       self.numFrames = numFrames 
  
class CannonBall(Object, pygame.sprite.Sprite):
    
    YTOCANNONY = 8 # sPACE BETWEEN y of cannon ball to y of cannon
    XTOCANNONX = -16 # sPACE BETWEEN y of cannon ball to y of cannon
    SPEED = 4
    FRAME_RATE_CHANGE_ANIM = 10
    WIDTH = 32
    HEIGHT = 32
    BOTTOM_SPACE = 0 # Space between foot and ground according to image size 
    ALIVE_STATE = 0
    EXPLODE_STATE = 1  
    
    def __init__(self, x, y, isFacingRight):
        super().__init__(x, y, self.WIDTH, self.HEIGHT, 'CannonBall')
        
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Idle/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Explosion/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Explosion/2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Explosion/3.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Explosion/4.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Explosion/5.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Explosion/6.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Ball Explosion/7.png'))) 
              
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i],(self.WIDTH, self.HEIGHT))
            if isFacingRight: 
                self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)
        
        self.animInfo = [AnimInfo(0, 1), AnimInfo(1, 7)]
        self.frameCount = 0 
        
        self.image = self.sprites[0]
        
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

        self.moveDistance = 0
        self.velocityX = self.SPEED if isFacingRight else -self.SPEED
        self.state = self.ALIVE_STATE
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, player):
        self.mask = pygame.mask.from_surface(self.image)
        #self.update_camera(player.velocity.x, player.move_camera)
        
        # Player die if touch ball (thay kill bang ham chuyen trang thai player die)
        if self.collide_player(player):
            self.kill()
        
        # Move cannon ball a distance == Cannon.SHOOTING_RANGE
        if self.state == self.ALIVE_STATE:
            self.move()
        
        # Animation
        if self.frameCount % 10 == 0:
            self.image = self.sprites[self.animInfo[self.state].startFrame + self.frameCount//10]
        self.frameCount += 1
        if self.frameCount > (self.animInfo[self.state].numFrames - 1)*10:
            if self.state == self.EXPLODE_STATE: 
                self.kill()
            else:
                self.frameCount = 0
                
    def move(self):
        self.rect.x += self.velocityX
        self.moveDistance += self.velocityX
        if self.moveDistance*self.moveDistance == Cannon.SHOOTING_RANGE*Cannon.SHOOTING_RANGE:
            self.explode()
    
    def explode(self):
        self.state = self.EXPLODE_STATE
        self.frameCount = 0
        
    def collide_player(self, player):
        return pygame.sprite.collide_rect(self, player)
           
class Cannon(Object, pygame.sprite.Sprite):   
    
    SHOOTING_FRAME_RATE = 120
    SHOOTING_RANGE = 400
    FRAME_RATE_CHANGE_ANIM = 10
    WIDTH = 80
    HEIGHT = 52
    BOTTOM_SPACE = 0 # Space between foot and ground according to image size 
    STAND_STATE = 0
    SHOOTING_STATE = 1  
    TAKE_DMG_STATE = 2
    DEAD_STATE = 3
    
    def __init__(self, x, y, isFacingRight):
        super().__init__(x, y, self.WIDTH, self.HEIGHT, 'Cannon')
        
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Idle/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/3.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/4.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/5.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/6.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Hit/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Hit/2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Hit/3.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Hit/4.png')))     
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/3.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/4.png')))          
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i],(self.WIDTH, self.HEIGHT))
            if isFacingRight: 
                self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)
        
        self.animInfo = [AnimInfo(0, 1), AnimInfo(1, 6), AnimInfo(7, 4), AnimInfo(11, 4)]
        self.frameCount = 0 
        
        self.image = self.sprites[0]
        
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

        self.frameCountShooting = 0
        self.isFacingRight = isFacingRight
        self.state = self.SHOOTING_STATE
        self.cannonBallGroup = pygame.sprite.Group()
        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 2

    def update(self, player):
        # Create mask to detect collision
        self.mask = pygame.mask.from_surface(self.image)
        # self.update_camera(player.velocity.x, player.move_camera)
        
        # Auto shoot every SHOOTING_FRAME_RATE
        if self.state != self.DEAD_STATE:
            if self.frameCountShooting == 0:
                self.shoot()
            self.frameCountShooting += 1
            if self.frameCountShooting == self.SHOOTING_FRAME_RATE:
                self.frameCountShooting = 0
        
        # Animation
        if self.frameCount % 10 == 0:
            self.image = self.sprites[self.animInfo[self.state].startFrame + self.frameCount//10]
        self.frameCount += 1
        if self.frameCount > (self.animInfo[self.state].numFrames - 1)*10:
            if self.state == self.DEAD_STATE: 
                self.kill()
            if self.state == self.TAKE_DMG_STATE:
                if self.hp <= 0:
                    self.dead()
                else:
                    self.stand()   
            if self.state == self.SHOOTING_STATE:
                self.cannonBallGroup.add(CannonBall(self.rect.x + self.WIDTH + CannonBall.XTOCANNONX if self.isFacingRight else self.rect.x + CannonBall.XTOCANNONX, self.rect.y + CannonBall.YTOCANNONY, self.isFacingRight))
                self.stand() 
            else:
                self.frameCount = 0
    
    def dead(self):
        self.state = self.DEAD_STATE
        self.frameCount = 0
        
    def stand(self):
        self.state = self.STAND_STATE
        self.frameCount = 0
        
    def shoot(self):
        self.state = self.SHOOTING_STATE
        self.frameCount = 0
     
    def take_dmg(self, dmg): # Immune when being taken dmg
        if self.state != self.TAKE_DMG_STATE:
            self.state = self.TAKE_DMG_STATE
            self.frameCount = 0    
            self.hp -= dmg   
        
    ############## Getters & Setters ##############
    def set_hp(self, hp):
        self.hp = hp     
    
    def get_hp(self):
        return self.hp