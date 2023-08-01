"""
Author : Rori Wu, Zenia Haroon

Date : 7/27/23

Description : Contains the CelesteEnvironment class and all of its functionality
"""
import pygame, sys
from pygame import *

block = pygame.image.load('art/Tile_White.png')
spikes = pygame.image.load('art/Tile_Spikes.png')
ledge = pygame.image.load('art/Tile_Ledge.png')
maddy = pygame.image.load('art/Hitbox_Maddy.png')
tilesize = block.get_height()
gamemap = [['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','1','1','0','0','0','0','0','2','2','2','2','2','2','0','0','0','0','1','1','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','0','0','0','0','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','0','0','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1',],
           ['1','1','1','1','1','1','0','0','0','0','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1',],
           ['1','1','1','1','0','1','0','0','0','0','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','3','3','1','1','1','1','1','1','1','1','1','1','1',],
           ['1','1','0','0','0','1','0','0','0','0','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1','1','1',],
           ['1','1','0','0','0','0','0','0','0','0','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1',],
           ['1','0','0','0','0','0','0','0','0','0','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1',],
           ['1','0','0','0','0','0','0','0','0','0','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1',],
           ['1','0','0','0','0','0','0','0','0','0','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','3','3','3','3','3','1','1','1','1','1','1','1','1','1',],
           ['1','0','0','0','0','0','0','0','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','1','1','1','1','1','1','1','1','1',],
           ['1','0','0','0','0','0','0','0','1','1','1','1','1','1','0','0','0','0','0','0','0','0','2','2','2','2','2','2','1','1','1','1','1','1','1','1','1','1','1','1',],
           ['1','0','0','0','0','0','0','0','1','1','1','1','1','1','2','2','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1',],
           ['1','3','3','3','1','1','1','1','1','1','1','1','1','1','1','1','2','2','2','2','2','2','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1',],
           ['1','0','0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1',]]
screendims = (640, 360)
dis = display.set_mode(screendims)
jumpmax_y = 3 * tilesize
jumpmax_x = 6 * tilesize
maxv_x = 1.5
maxv_y = 5
gravity = (2 * jumpmax_y * maxv_y * maxv_y) / (jumpmax_x * jumpmax_x)

class CelesteEnvironment:

    #Initializes the CelesteEnvironment class
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Celeste")
        self.screen = pygame.Surface((320, 180))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.x = 0
        self.y = 0
        self.maddy_rect = pygame.Rect(16, 156, maddy.get_width(), maddy.get_height())
        self.maddy_pos = [self.maddy_rect.x, self.maddy_rect.y]
        self.maddy_xvelocity = 0
        self.maddy_yvelocity = 0
        self.maddy_yaccel = 0
        self.movingright = False
        self.movingleft = False
        self.hasdash = True
        self.inair = False
        self.isclimbing = False
        self.pastjumppeak = False
        self.stamina_max = 110
        self.tilerects = []
        self.collisiontypes = {'top': False, 'bottom': False, 'right': False, 'left': False}

    #Updates time, updates game
    def step(self, action):
        self.maddy_update()
        self.get_playeraction(action)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 return True
            if event.type == KEYDOWN:
                if event.key == K_c:
                    self.jump()
                if event.key == K_RIGHT:
                    self.movingright = True
                if event.key == K_LEFT:
                    self.movingleft = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.movingright = False
                if event.key == K_LEFT:
                    self.movingleft = False
                if event.key == K_z:
                    self.isclimbing = False
        self.dt = self.clock.tick(60)/1000
        return False

    #Updates madeline's position
    def maddy_update(self):
        self.move_collision()
        self.maddy_rect.x = self.maddy_pos[0]
        self.maddy_rect.y = self.maddy_pos[1]
        if self.maddy_yvelocity > 0:
            self.pastjumppeak = True
        else:
            self.pastjumppeak = False
        if self.collisiontypes['bottom']:
            self.inair = False
        elif not self.isclimbing:
            if self.pastjumppeak:
                self.maddy_yvelocity += gravity * 16 * self.dt 
            else:
                self.maddy_yvelocity += gravity * 19.2 * self.dt
            self.inair = True

    def jump(self):
        if not(self.inair):
            self.maddy_yvelocity = 0
            self.maddy_yvelocity -= 1.2 * jumpmax_y * (maxv_y / (jumpmax_x))
        #add walljumping and neutrals
        """
        elif self.collisiontypes['right']:
            self.maddy_yvelocity = 0
            self.maddy_yvelocity -= 1.6 * jumpmax_y * (maxv_y / (jumpmax_x))
        elif self.collisiontypes['left']:
            self.maddy_yvelocity = 0
            self.maddy_yvelocity -= 1.6 * jumpmax_y * (maxv_y / (jumpmax_x))
        """

    #Returns a list of all object collisions
    def collision(self):
        collisionlist = []
        for tile in self.tilerects:
            if pygame.Rect.colliderect(self.maddy_rect, tile):
                collisionlist.append(tile)
        return collisionlist

    #Adjusts Maddy's position to represent collisions
    def move_collision(self):
        self.collisiontypes = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.maddy_rect.x += self.maddy_xvelocity
        self.maddy_pos[0] += self.maddy_xvelocity
        collisions = self.collision()
        for tile in collisions:
            if self.maddy_xvelocity > 0:
                self.maddy_rect.right = self.maddy_pos[0] = tile.left
                self.maddy_pos[0] -= maddy.get_width()
                self.collisiontypes['right'] = True
            elif self.maddy_xvelocity < 0:
                self.maddy_rect.left = self.maddy_pos[0] = tile.right
                self.collisiontypes['left'] = True
        self.maddy_rect.y += self.maddy_yvelocity
        self.maddy_pos[1] += self.maddy_yvelocity
        collisions = self.collision()
        for tile in collisions:
            if self.maddy_yvelocity > 0:
                self.maddy_rect.bottom = self.maddy_pos[1] = tile.top
                self.maddy_pos[1] -= maddy.get_height()
                self.collisiontypes['bottom'] = True
            elif self.maddy_yvelocity < 0:
                self.maddy_rect.top = self.maddy_pos[1] = tile.bottom
                self.collisiontypes['top'] = True
        
    #Renders all visuals
    def render(self):
        self.screen.fill("black")
        self.y = 0
        self.screen.blit(maddy, (self.maddy_pos[0], self.maddy_pos[1]))
        self.tilerects = []
        for row in gamemap:
            self.x = 0
            for tile in row:
                if tile == '1':
                    self.screen.blit(block, (self.x*tilesize, self.y*tilesize))
                elif tile == '2':
                    self.screen.blit(spikes, (self.x*tilesize, self.y*tilesize))
                elif tile == '3':
                    self.screen.blit(ledge, (self.x*tilesize, self.y*tilesize))
                if tile != '0':
                    self.tilerects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, tilesize, tilesize))
                self.x += 1
            self.y += 1 
        surf = pygame.transform.scale(self.screen, (640, 360))
        dis.blit(surf, (0, 0))
        pygame.display.flip()

    #Dictates the actions of the player 
    def get_playeraction(self, action):
        if action[pygame.K_z]:
            print(self.collisiontypes)
            if self.collisiontypes['left'] or self.collisiontypes['right']:
                self.isclimbing = True
        if self.isclimbing:
            if not(action[pygame.K_UP] and action[pygame.K_DOWN]):
                if action[pygame.K_UP]:
                    self.maddy_yvelocity = -1
                elif action[pygame.K_DOWN]:
                    self.maddy_yvelocity = 1
                else:
                    self.maddy_yvelocity = 0
            else:
                self.maddy_yvelocity = 0
        if not(self.movingleft and self.movingright):
            if self.movingright:
                self.maddy_xvelocity = maxv_x
            elif self.movingleft:
                self.maddy_xvelocity = -maxv_x
            else:
                self.maddy_xvelocity = 0
        else:
            self.maddy_xvelocity = 0

    #Quits the game
    @staticmethod
    def close():
        pygame.quit()
    
    #Returns player input
    @staticmethod
    def get_playerinput():
        return pygame.key.get_pressed()