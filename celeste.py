"""
Author : Rori Wu, Zenia Haroon

Date : 7/27/23

Description : Contains the CelesteEnvironment class and all of its functionality
"""
import math as mth
dashspeed = 3.4
diagonaldashspeed = mth.sqrt(dashspeed)

import pygame, sys
from pygame import *

#Screen
screendims = (640, 360)
dis = display.set_mode(screendims)

#Visuals
block = pygame.image.load('art/Tile_White.png').convert_alpha()
spikes = pygame.image.load('art/Tile_Spikes.png').convert_alpha()
ledge = pygame.image.load('art/Tile_Ledge.png').convert_alpha()
dashcrystal = pygame.image.load('art/Tile_Dashcrystal.png').convert_alpha()
dashcrystal_used = pygame.image.load('art/Tile_Dashcrystal_Used.png').convert_alpha()
maddy = pygame.image.load('art/Maddy_Body.png').convert_alpha()
maddy_tired = pygame.image.load('art/Maddy_Body_Flashred.png').convert_alpha()
maddy_hair_red = pygame.image.load('art/Maddy_Hair_Red.png').convert_alpha()
maddy_hair_blue = pygame.image.load('art/Maddy_Hair_Blue.png').convert_alpha()
tilesize = block.get_height()
gamemap = [['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['1','1','1','1','1','0','0','0','0','0','2','2','2','2','2','2','0','0','0','0','1','1','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','0','0','0','0','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
           ['0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','0','4','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
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

#Gravity
jumpmax_y = 3 * tilesize
jumpmax_x = 6 * tilesize
maxv_x = 1.5
maxv_y = 5
gravity = (2 * jumpmax_y * maxv_y * maxv_y) / (jumpmax_x * jumpmax_x)

#Parameters
stamina_max = 110
maxfall = 2.3
dashtime = .25
walljumpmax = 14
walljumpextendmax = 24
crystaltime = 2.6

levelstartpos = (16, 156)
spikeson = True

class CelesteEnvironment:

    #Initializes the CelesteEnvironment class
    def __init__(self):

        #Setup
        pygame.init()
        pygame.display.set_caption("Celeste")
        self.screen = pygame.Surface((320, 180))

        #Time
        self.clock = pygame.time.Clock()
        self.dt = 0

        #Coordinates
        self.x = 0
        self.y = 0

        #Maddy hitbox
        self.maddy_rect = pygame.Rect(levelstartpos[0], levelstartpos[1], maddy.get_width(), maddy.get_height())
        
        #Maddy's true position
        self.maddy_pos = [self.maddy_rect.x, self.maddy_rect.y]

        #Vertical and horizontal movement
        self.maddy_xvelocity = 0
        self.maddy_yvelocity = 0
        self.movingright = False
        self.movingleft = False

        #Jumping
        self.pastjumppeak = False
        self.inair = False

        #Walljumping
        self.againstwall = [False, ""]
        self.lockedmovement = [False, ""]
        self.walljumppos = 0
        self.walljumpdistance = walljumpmax

        #Climbing
        self.istired = False
        self.cangrab = True
        self.isclimbingup = False
        self.isgrabbing = False
        self.stamina = stamina_max
        self.flashingcounter = 0

        #Dashing
        self.dashbuffer = 4
        self.dashcountdown = False
        self.hasdash = True
        self.isdashing = False
        self.dashdirection = ""
        self.dashtimer = dashtime
        self.crystalused = False
        self.crystaltimer = crystaltime

        #Directional input
        self.isfacing = ""
        self.islooking = ""

        #Death
        self.isdead = False
        self.deathcount = 0
        
        #Collisions
        self.tilerects = []
        self.spikerects = []
        self.ledgerects = []
        self.crystalrects = []
        self.collisiontypes = {'TOP': False, 'BOTTOM': False, 'RIGHT': False, 'LEFT': False}
        self.isdead = False
        self.deathcount = 0

    #Updates game
    def step(self, action):
        self.maddy_update(action)
        self.get_playeraction(action)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 return True
            if event.type == KEYDOWN:
                if event.key == K_c:
                    self.jump()
                if event.key == K_x:
                    self.dashcountdown = True
                if event.key == K_RIGHT:
                    self.movingright = True
                if event.key == K_LEFT:
                    self.movingleft = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.isfacing = "RIGHT"
                    self.movingright = False
                if event.key == K_LEFT:
                    self.isfacing = "LEFT"
                    self.movingleft = False
                if event.key == K_z:
                    self.isgrabbing = False
         
        self.dt = self.clock.tick_busy_loop(60)/1000
        return False
            
    #Updates Madeline's position
    def maddy_update(self, action):
        self.move_collision()
        self.maddy_rect.x = self.maddy_pos[0]
        self.maddy_rect.y = self.maddy_pos[1]
        self.check_jump()
        self.check_dash(action)
        self.check_fallstate()
        self.update_stamina()
        self.update_crystal()
        if self.isdead:
            self.ondeath()

    #Resets Madeline's position upon death
    def ondeath(self):
        self.deathcount += 1
        self.maddy_pos[0] = levelstartpos[0]
        self.maddy_pos[1] = levelstartpos[1]
        self.maddy_rect.x = self.maddy_pos[0]
        self.maddy_rect.y = self.maddy_pos[1]
        self.isdead = False

    #Checks to see if a dash crystal should refresh
    def update_crystal(self):
        if self.crystalused:
            self.crystaltimer -= self.dt
            if self.crystaltimer <= 0:
                self.crystalused = False
                self.crystaltimer = crystaltime

    #Checks if a jump is past its peak
    def check_jump(self):
        jumpdistance = self.walljumppos - self.maddy_pos[0]
        if (jumpdistance >= self.walljumpdistance) or (jumpdistance <= -self.walljumpdistance):
            self.lockedmovement = [False, ""]
            self.walljumpdistance = walljumpmax
        if self.maddy_yvelocity > 0:
            self.pastjumppeak = True
        else:
            self.pastjumppeak = False

    #Checks if Madeline is dashing
    def check_dash(self, action):
        if self.dashcountdown:
            self.dashbuffer -= 1
            if self.dashbuffer == 0:
                self.move_dash(action)
                self.dashbuffer = 4
                self.dashcountdown = False
        if self.isdashing and self.dashtimer > 0:
            self.dash()
            self.dashtimer -= self.dt
        elif self.isdashing:
            self.dashtimer = dashtime
            self.isdashing = False
            if self.maddy_yvelocity < 0:
                self.maddy_yvelocity = -.5
            self.maddy_xvelocity = 0

    #Checks to see if Madeline is in the air
    def check_fallstate(self):
        if self.collisiontypes['BOTTOM']:
            self.inair = False
            self.stamina = stamina_max
            self.istired = False
            self.cangrab = True
            if not self.isdashing:
                self.hasdash = True
        elif not self.isgrabbing and not self.isdashing:
            self.add_gravity()
            self.inair = True

    #Refreshes Madeline's dash upon touching a dash crystal
    def check_crystal(self):
        if not self.crystalused:
            if not self.hasdash:
                self.hasdash = True
                self.stamina = stamina_max
            elif self.istired:
                self.stamina = stamina_max
            self.istired = False
            self.crystalused = True

    #Updates stamina
    def update_stamina(self):
        if self.isclimbingup:
            self.stamina -= self.dt * 45.45
        elif self.isgrabbing:
            self.stamina -= self.dt * 10
        if self.stamina < 0:
            self.stamina = 0
        if self.stamina <= 20:
            self.istired = True
        if self.stamina == 0:
            self.isgrabbing = False
            self.cangrab = False
            self.isclimbingup = False
    
    #Implements gravity
    def add_gravity(self):
        if self.pastjumppeak:
            self.maddy_yvelocity += gravity * 14 * self.dt 
        else:
            self.maddy_yvelocity += gravity * 16.8 * self.dt
        if self.maddy_yvelocity > maxfall:
            self.maddy_yvelocity = maxfall

    #Jump mechanics
    def jump(self):
        if not self.inair and not self.isgrabbing:
            self.maddy_yvelocity = 0
            self.maddy_yvelocity -= 1.1 * jumpmax_y * (maxv_y / (jumpmax_x))
        elif self.againstwall[0]:
            self.walljumppos = self.maddy_pos[0]
            self.lockedmovement[0] = True
            self.maddy_yvelocity = 0
            self.maddy_yvelocity -= 1.1 * jumpmax_y * (maxv_y / (jumpmax_x)) 
            if self.againstwall[1] == "RIGHT":
                self.lockedmovement[1] = "LEFT"
            elif self.againstwall[1] == "LEFT":
                self.lockedmovement[1] = "RIGHT"

    #Dash mechanics
    def dash(self):
        if self.dashdirection == "RIGHT":
            self.maddy_xvelocity = dashspeed
            self.maddy_yvelocity = 0
        elif self.dashdirection == "LEFT":
            self.maddy_xvelocity = -dashspeed
            self.maddy_yvelocity = 0
        elif self.dashdirection == "UP":
            self.maddy_xvelocity = 0
            self.maddy_yvelocity = -dashspeed
        elif self.dashdirection == "DOWN":
            self.maddy_xvelocity = 0
            self.maddy_yvelocity = dashspeed
        elif self.dashdirection == "UPRIGHT":
            self.maddy_xvelocity = diagonaldashspeed
            self.maddy_yvelocity = -diagonaldashspeed
        elif self.dashdirection == "DOWNRIGHT":
            self.maddy_xvelocity = diagonaldashspeed
            self.maddy_yvelocity = diagonaldashspeed
        elif self.dashdirection == "UPLEFT":
            self.maddy_xvelocity = -diagonaldashspeed
            self.maddy_yvelocity = -diagonaldashspeed
        elif self.dashdirection == "DOWNLEFT":
            self.maddy_xvelocity = -diagonaldashspeed
            self.maddy_yvelocity = diagonaldashspeed

    #Sets dash direction
    def dash_direction(self, directions):
        self.dashdirection = ""
        if self.hasdash:
            self.hasdash = False
            self.isdashing = True
            if not("RIGHT" in directions and "LEFT" in directions) and not("UP" in directions and "DOWN" in directions):
                if "RIGHT" in directions:
                    if "UP" in directions:
                        self.dashdirection = "UPRIGHT"
                    elif "DOWN" in directions:
                        self.dashdirection = "DOWNRIGHT"
                    else:
                        self.dashdirection = "RIGHT"
                elif "LEFT" in directions:
                    if "UP" in directions:
                        self.dashdirection = "UPLEFT"
                    elif "DOWN" in directions:
                        self.dashdirection = "DOWNLEFT"
                    else:
                        self.dashdirection = "LEFT"
                elif "UP" in directions:
                    self.dashdirection = "UP"
                elif "DOWN" in directions:
                    self.dashdirection = "DOWN"
                else:
                    if self.islooking == "UP":
                        self.dashdirection = "UP"
                    elif self.islooking == "DOWN":
                        self.dashdirection = "DOWN"
                    elif self.isfacing == "RIGHT":
                        self.dashdirection = "RIGHT"
                    elif self.isfacing == "LEFT":
                        self.dashdirection = "LEFT"
                    else:
                        self.dashdirection = "RIGHT"

    #Returns a list of all object collisions
    def collision(self):
        collisionlist = []
        for tile in self.tilerects:
            if pygame.Rect.colliderect(self.maddy_rect, tile):
                collisionlist.append(tile)
        return collisionlist

    #Checks to see if Madeline is colliding with spikes
    def spike_collision(self):
        for tile_rect in self.spikerects:
            if tile_rect.colliderect(self.maddy_rect):
                if spikeson:
                    self.isdead = True

    #Checks to see if Madeline is colliding with ledges
    def ledge_collision(self):
        for ledge_rect in self.ledgerects:
            if ledge_rect.colliderect(self.maddy_rect) and self.maddy_yvelocity > 0:
                self.maddy_rect.bottom = self.maddy_pos[1] = ledge_rect.top
                self.maddy_pos[1] -= maddy.get_height()
                self.collisiontypes['BOTTOM'] = True

    #Checks to see if Madeline is colliding with a dash crystal
    def crystal_collision(self):
        for tile_rect in self.crystalrects:
            if tile_rect.colliderect(self.maddy_rect):
                self.check_crystal()

    #Implements collisions
    def move_collision(self):
        isagainstright = False
        isagainstleft = False
        self.collisiontypes = {'TOP': False, 'BOTTOM': False, 'RIGHT': False, 'LEFT': False}
        self.maddy_rect.x += self.maddy_xvelocity
        self.maddy_pos[0] += self.maddy_xvelocity
        collisions = self.collision()
        self.spike_collision()
        self.crystal_collision()
        for tile in collisions:
            if self.maddy_xvelocity > 0:
                self.maddy_rect.right = self.maddy_pos[0] = tile.left
                self.maddy_pos[0] -= maddy.get_width()
                self.collisiontypes['RIGHT'] = True
            elif self.maddy_xvelocity < 0:
                self.maddy_rect.left = self.maddy_pos[0] = tile.right
                self.collisiontypes['LEFT'] = True
        self.maddy_rect.y += self.maddy_yvelocity
        self.maddy_pos[1] += self.maddy_yvelocity
        collisions = self.collision()
        self.spike_collision()
        self.ledge_collision()
        self.crystal_collision()
        for tile in collisions:
            if self.maddy_yvelocity > 0:
                self.maddy_rect.bottom = self.maddy_pos[1] = tile.top
                self.maddy_pos[1] -= maddy.get_height()
                self.collisiontypes['BOTTOM'] = True
            elif self.maddy_yvelocity < 0:
                self.maddy_rect.top = self.maddy_pos[1] = tile.bottom
                self.collisiontypes['TOP'] = True
                self.maddy_yvelocity = 0
        for tile in self.tilerects:   
            self.maddy_rect.x += 1
            if pygame.Rect.colliderect(self.maddy_rect, tile):
                isagainstright = True
            self.maddy_rect.x -= 2
            if pygame.Rect.colliderect(self.maddy_rect, tile):
                isagainstleft = True
            self.maddy_rect.x += 1
        if isagainstright:
            self.againstwall = [True, "RIGHT"]
        elif isagainstleft:
            self.againstwall = [True, "LEFT"]
        else:
            self.againstwall = [False, ""]

    #Renders all visuals
    def render(self):
        self.screen.fill("black")
        self.render_maddy()
        self.render_gamemap()
        surf = pygame.transform.scale(self.screen, (640, 360))
        dis.blit(surf, (0, 0))
        pygame.display.flip()

    #Renders Madeline
    def render_maddy(self):
        if self.istired:
            if self.flashingcounter == 0:
                self.screen.blit(maddy_tired, (self.maddy_pos[0], self.maddy_pos[1]))
                self.flashingcounter += 1
            else:
                self.screen.blit(maddy, (self.maddy_pos[0], self.maddy_pos[1]))
                self.flashingcounter -= 1
        else:
            self.screen.blit(maddy, (self.maddy_pos[0], self.maddy_pos[1]))
        if self.hasdash:
            self.screen.blit(maddy_hair_red, (self.maddy_pos[0], self.maddy_pos[1] - 3))
        else:
            self.screen.blit(maddy_hair_blue, (self.maddy_pos[0], self.maddy_pos[1] - 3))

    #Renders the game map
    def render_gamemap(self):
        self.y = 0
        self.tilerects = []
        self.spikerects = []
        self.ledgerects = []
        self.crystalrects = []
        bob_height = 4
        for row in gamemap:
            self.x = 0
            for tile in row:
                if tile == '1':
                    self.screen.blit(block, (self.x*tilesize, self.y*tilesize))
                elif tile == '2':
                    self.screen.blit(spikes, (self.x*tilesize, self.y*tilesize))
                elif tile == '3':
                    self.screen.blit(ledge, (self.x*tilesize, self.y*tilesize))
                elif tile == '4':     
                    bob_offset = bob_height * mth.sin(mth.radians(pygame.time.get_ticks() * 0.15)) 
                    if not self.crystalused:
                        self.screen.blit(dashcrystal, (self.x*tilesize, self.y*tilesize + 2 + bob_offset))
                    else:
                        self.screen.blit(dashcrystal_used, (self.x*tilesize, self.y*tilesize + 2 + bob_offset))               
                    self.crystalrects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, tilesize*2, tilesize*2))
                    
                if tile == '2':
                    self.spikerects.append(pygame.Rect(self.x*tilesize, self.y*tilesize + 5, tilesize, tilesize - 5))
                elif tile == '3':
                    self.ledgerects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, tilesize, tilesize - 7))
                elif tile == '4':
                    self.crystalrects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, tilesize*2, tilesize*2))
                elif tile != '0':
                    self.tilerects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, tilesize, tilesize))
                self.x += 1            
            self.y += 1 

    #Performs player actions
    def get_playeraction(self, action):
        self.move_climb(action)
        self.move_leftright()
        self.move_look(action)

    #Assigns climbing movement
    def move_climb(self, action):
        if action[pygame.K_z]:
            if self.cangrab:
                if self.collisiontypes['LEFT'] or self.collisiontypes['RIGHT']:
                    self.isgrabbing = True
                else:
                    self.isgrabbing = False
                    if self.istired:
                        self.cangrab = False
        if self.isgrabbing:
            if not(action[pygame.K_UP] and action[pygame.K_DOWN]):
                if action[pygame.K_UP]:
                    self.maddy_yvelocity = -.8
                    self.isclimbingup = True
                elif action[pygame.K_DOWN]:
                    self.maddy_yvelocity = 1.4
                    self.isclimbingup = False
                else:
                    self.maddy_yvelocity = 0
                    self.isclimbingup = False
            else:
                self.maddy_yvelocity = 0

    #Assigns left-right movement
    def move_leftright(self):
        if not self.isdashing and not self.isgrabbing:
            if not(self.movingleft and self.movingright):
                if self.lockedmovement[0]:
                    if self.lockedmovement[1] == "RIGHT":
                        self.maddy_xvelocity = maxv_x
                        if self.movingleft:
                            self.walljumpdistance = walljumpextendmax
                    elif self.lockedmovement[1] == "LEFT":
                        self.maddy_xvelocity = -maxv_x
                        if self.movingright:
                            self.walljumpdistance = walljumpextendmax
                elif self.movingright:
                    self.maddy_xvelocity = maxv_x
                elif self.movingleft:
                    self.maddy_xvelocity = -maxv_x
                else:
                    self.maddy_xvelocity = 0
            else:
                self.isfacing = "False"
                self.maddy_xvelocity = 0

    #Assigns looking up and down
    def move_look(self, action):
        if not(action[pygame.K_UP] and action[pygame.K_DOWN]):
            if action[pygame.K_UP]:
                self.islooking = "UP"
            elif action[pygame.K_DOWN]:
                self.islooking = "DOWN"
            else:
                self.islooking = "False"

    #Assigns dash directions
    def move_dash(self, action):
        directions = []
        if action[pygame.K_RIGHT]:
            directions.append("RIGHT")
        if action[pygame.K_LEFT]:
            directions.append("LEFT")
        if action[pygame.K_UP]:
            directions.append("UP")
        if action[pygame.K_DOWN]:
            directions.append("DOWN")
        self.dash_direction(directions)

    #Quits the game
    @staticmethod
    def close():
        pygame.quit()
    
    #Returns player input
    @staticmethod
    def get_playerinput():
        return pygame.key.get_pressed()