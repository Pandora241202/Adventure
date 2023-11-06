import pygame
import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 384
SCROLL_THRESHOLD_X = 768
SCROLL_THRESHOLD_Y = 300
SCREEN_COUNT = 2

class AnimInfo():
   def __init__(self, startFrame, numFrames):
       self.startFrame = startFrame
       self.numFrames = numFrames 

class Player(pygame.sprite.Sprite):
    
    GRAVITY = 1
    START_SPEED = 1
    SPEED = 6
    JUMP_SPEED = -8
    FPS = 60
    FRICTION_FORCE = 1
    ATTACK_RANGE = 32
    FRAME_RATE_CHANGE_SPEED_X = 5
    FRAME_RATE_CHANGE_SPEED_Y = 5
    FRAME_RATE_CHANGE_ANIM = 10
    WIDTH = 64*2
    HEIGHT = 40*2
    BOTTOM_SPACE = 8*2 # Space between foot and ground according to image size 
    TOP_SPACE = 4*2
    LEFT_SPACE = 24*2
    RIGHT_SPACE = 24*2
    IDLE_STATE = 0
    RUN_STATE = 1  
    JUMP_STATE = 2
    FALL_STATE = 3
    DEAD_STATE = 4
    
    def __init__(self, x, y):
        super().__init__()
        self.frame_count_change_speed = -1
        
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Idle Sword/Idle Sword 01.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Idle Sword/Idle Sword 02.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Idle Sword/Idle Sword 03.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Idle Sword/Idle Sword 04.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Idle Sword/Idle Sword 05.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Run Sword/Run Sword 01.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Run Sword/Run Sword 02.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Run Sword/Run Sword 03.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Run Sword/Run Sword 04.png')))  
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Run Sword/Run Sword 05.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Run Sword/Run Sword 06.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Jump Sword/Jump Sword 01.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Jump Sword/Jump Sword 02.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Jump Sword/Jump Sword 03.png')))    
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Fall Sword/Fall Sword 01.png')))   
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Dead Hit/Dead Hit 01.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Dead Hit/Dead Hit 02.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Player', 'Dead Hit/Dead Hit 03.png')))
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i],(self.WIDTH, self.HEIGHT))
        
        self.animInfo = [AnimInfo(0, 5), AnimInfo(5, 6), AnimInfo(11, 3), AnimInfo(14, 1), AnimInfo(15, 4)]
        self.frameCount = 0 
        
        self.image = self.sprites[0]
        
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.x = x
        self.y = y + 64 ##########*
        self.velocity = pygame.math.Vector2(0, 0)
        self.fall_count = 0 # virtual gravity

        self.isFacingRight = True
        self.state = self.IDLE_STATE
        self.mask = None
           
        # Cooldown & Timer
        self.dash_cd_timer = 0
        self.dash_cd = 1
        
        self.move_camera = False
        
        self.frameCount = 0
        self.frame_count_change_speed_x = -1
        self.frame_count_change_speed_y = -1
       
    def update(self, keys, objects):
        
        # Control keys
        self.update_input(keys)

        #self.update_cd_timer()
        
        # Land on the ground
        if self.frame_count_change_speed_y == -1 and self.state == self.FALL_STATE:
            self.idle()
        
        # Change speed vertically
        if self.frame_count_change_speed_y != -1:
            if self.frame_count_change_speed_y % self.FRAME_RATE_CHANGE_SPEED_Y == 0:   
                self.velocity.y += 1  
            self.frame_count_change_speed_y += 1       
            
        # Fall when jump speed >= 0
        if self.state == self.JUMP_STATE and self.velocity.y >= 0:
            self.fall()
        
        # Try to do somethong when colide verticle with block
        self.vertical_collision(objects)
        
        # Try to land when fall
        if self.state == self.FALL_STATE: 
            self.land_when_fall(objects)
        
        # Fall when run into space
        if self.state == self.RUN_STATE and not self.on_ground(objects):
            self.fall()
        
        # Change rect   
        self.move()
        
        # Scroll
        scrollX = 0
        scrollY = 0 
        if self.x >= SCREEN_WIDTH - SCROLL_THRESHOLD_X and self.x <= SCREEN_WIDTH*SCREEN_COUNT - SCROLL_THRESHOLD_X:
            self.rect.x -= self.velocity.x
            scrollX = -self.velocity.x   
        if self.y >= SCREEN_HEIGHT - SCROLL_THRESHOLD_Y and self.y <= SCREEN_HEIGHT*SCREEN_COUNT - SCROLL_THRESHOLD_Y:
            self.rect.y -= self.velocity.y
            scrollY = -self.velocity.y
            
        # Animation
        if self.frameCount % 10 == 0:
            self.image = self.sprites[self.animInfo[self.state].startFrame + self.frameCount//self.FRAME_RATE_CHANGE_ANIM]
        self.frameCount += 1
        if self.frameCount > (self.animInfo[self.state].numFrames - 1)*self.FRAME_RATE_CHANGE_ANIM:
            if self.state == self.DEAD_STATE: 
                self.kill()
            self.frameCount = 0
        
        return (scrollX, scrollY)
        
    def move(self):
        self.rect.x += self.velocity.x
        self.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.y += self.velocity.y
        if self.x < 0: 
            self.x = 0
            self.rect.x = 0
        if self.x + self.WIDTH > SCREEN_WIDTH*SCREEN_COUNT: 
            self.x = SCREEN_WIDTH*SCREEN_COUNT - self.WIDTH
            self.rect.x = SCREEN_WIDTH - self.WIDTH
            
    def flip(self):
        self.isFacingRight = not self.isFacingRight
        self.velocity.x = self.START_SPEED if self.isFacingRight else -self.START_SPEED
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)

    def update_input(self, input_keys):
        # Move left right
        if input_keys[pygame.K_LEFT] or input_keys[pygame.K_RIGHT]:
            # Change direction
            if (input_keys[pygame.K_LEFT] and self.isFacingRight) or (input_keys[pygame.K_RIGHT] and not self.isFacingRight):
                self.flip()
            
            # Change state to run if player is not moving
            if self.state == self.IDLE_STATE:
                self.run()
            
            # Increase speed horizontally
            if self.velocity.x <= -self.SPEED or self.velocity.x >= self.SPEED:
                self.velocity.x = self.SPEED if self.isFacingRight else -self.SPEED
            else:
                if self.frame_count_change_speed_x % self.FRAME_RATE_CHANGE_SPEED_X == 0:    
                    self.velocity.x += 1 if self.isFacingRight else -1
                self.frame_count_change_speed_x += 1
        else:
            # Decrease speed horizontally
            if self.frame_count_change_speed_x != -1:
                if self.frame_count_change_speed_x % self.FRAME_RATE_CHANGE_SPEED_X == 0:    
                    self.velocity.x -= 1 if self.isFacingRight else -1  
                self.frame_count_change_speed_x += 1
                if (self.velocity.x <= 0 and self.isFacingRight) or (self.velocity.x >= 0 and not self.isFacingRight):
                    self.frame_count_change_speed_x = -1
                    if self.state == self.RUN_STATE:
                        self.idle()        
        
        # Jump
        if input_keys[pygame.K_UP] and self.state != self.JUMP_STATE and self.state != self.FALL_STATE:
            self.jump()
        # # attack
        # elif input_keys[pygame.K_j]:
        #     pass
        # # dash
        # elif input_keys[pygame.K_k] or input_keys[pygame.K_LSHIFT] or input_keys[pygame.K_LCTRL]:
        #     if self.dash_cd_timer <= 0:
        #         self.velocity.x *= 3
        #         self.dash_cd_timer = self.dash_cd
        # # pull_skill
        # elif input_keys[pygame.K_e]:
        #     self.attack()
    
    def update_cd_timer(self):
        self.dash_cd_timer -= 1 / self.FPS
    
    def land_when_fall(self, blocks): 
        for block in blocks:
            newPosLeft = self.rect.x + self.velocity.x + (self.LEFT_SPACE if self.isFacingRight else self.RIGHT_SPACE)
            newPosRight = self.rect.x + self.WIDTH + self.velocity.x - (self.LEFT_SPACE if self.isFacingRight else self.RIGHT_SPACE)         
            if (newPosLeft >= block.rect.x and newPosLeft < block.rect.x + block.WIDTH) or (newPosRight > block.rect.x and newPosRight <= block.rect.x + block.WIDTH):
                if self.rect.y + self.HEIGHT - self.BOTTOM_SPACE < block.rect.y and self.rect.y + self.velocity.y + self.HEIGHT - self.BOTTOM_SPACE >= block.rect.y:
                    self.velocity.y = block.rect.y - self.rect.y - self.HEIGHT + self.BOTTOM_SPACE
                    self.frame_count_change_speed_y = -1
                    return

    def on_ground(self, blocks):
        for block in blocks:
            newPosLeft = self.rect.x + self.velocity.x + (self.LEFT_SPACE if self.isFacingRight else self.RIGHT_SPACE)
            newPosRight = self.rect.x + self.WIDTH + self.velocity.x - (self.LEFT_SPACE if self.isFacingRight else self.RIGHT_SPACE)         
            if (newPosLeft >= block.rect.x and newPosLeft < block.rect.x + block.WIDTH) or (newPosRight > block.rect.x and newPosRight <= block.rect.x + block.WIDTH):
                if self.rect.y + self.HEIGHT - self.BOTTOM_SPACE == block.rect.y:
                    return True
        return False
    
    def hit_head(self):
        self.fall_count = 0
        self.velocity.y = -1
        
    def vertical_collision(self, blocks):
        newPosTop = self.rect.y + self.TOP_SPACE
        newPosBottom = self.rect.y + self.HEIGHT - self.BOTTOM_SPACE
        if self.isFacingRight:
            curPosRight = self.rect.x + self.WIDTH - self.LEFT_SPACE           
            newPosRight = curPosRight + self.velocity.x
            for block in blocks:
                if (newPosTop >= block.rect.y and newPosTop < block.rect.y + block.HEIGHT) or (newPosBottom > block.rect.y and newPosBottom <= block.rect.y + block.HEIGHT):
                    if curPosRight <= block.rect.x and newPosRight >= block.rect.x:
                        self.velocity.x = block.rect.x - curPosRight
                        return
        else:
            curPosLeft = self.rect.x + self.RIGHT_SPACE
            newPosLeft = curPosLeft + self.velocity.x           
            for block in blocks:
                if (newPosTop >= block.rect.y and newPosTop < block.rect.y + block.HEIGHT) or (newPosBottom > block.rect.y and newPosBottom <= block.rect.y + block.HEIGHT):
                    if curPosLeft >= block.rect.x + block.WIDTH  and newPosLeft <= block.rect.x + block.WIDTH:
                        self.velocity.x = block.rect.x + block.WIDTH - curPosLeft
                        return
    
    def idle(self):
        self.velocity.x = 0
        self.velocity.y = 0
        self.state = self.IDLE_STATE
        self.frameCount = 0
        self.frame_count_change_speed_x = -1
    
    def run(self):
        self.state = self.RUN_STATE
        self.frameCount = 0
        self.frame_count_change_speed_x = 0
    
    def jump(self):
        self.state = self.JUMP_STATE
        self.velocity.y = self.JUMP_SPEED
        self.frameCount = 0
        self.frame_count_change_speed_y = 0
        
    def fall(self):
        self.state = self.FALL_STATE
        self.velocity.y = 0
        self.frameCount = 0
        self.frame_count_change_speed_y = 0
    
    ############## Getters & Setters ##############
    def set_hp(self, hp):
        self.hp = hp     
    
    def get_hp(self):
        return self.hp
        
    def get_tag(self):
        return self.tag

# Ref https://github.com/techwithtim/Python-Platformer/