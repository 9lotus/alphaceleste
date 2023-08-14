"""
Author : Rori Wu, Zenia Haroon

Date : 7/27/23 - TBD

Description : Contains the CelesteEnvironment class and all of its functionality
"""

import math as mth
import yaml
import numpy as np
import pygame, sys
from pygame import *

#yaml configs
with open("./config/game_parameters.yaml", 'r') as stream:
    out = yaml.safe_load(stream)
agent_config = out['agent']
screen_config = out['screen']
font_config = out['font']
framerate_config = out['framerate']
movement_config = out['movement']
gravity_config = out['gravity']
jumping_config = out['jumping']
climbing_config = out['climbing']
dashing_config = out['dashing']
crystal_config = out['crystal']
level_config = out['level']
with open("./config/map.yaml", 'r') as stream:
    out = yaml.safe_load(stream)
map_config = out['screens']

#Screen
screendims = screen_config[0]
gamedims = screen_config[1]
dis = display.set_mode(screendims)
screencolor = screen_config[2]

#Font
myfont = (font_config[0], font_config[1])

#Framerate
fps = framerate_config[0]

#Visuals
block = pygame.image.load('art/Tile_White.png').convert_alpha()
spikes = pygame.image.load('art/Tile_Spikes.png').convert_alpha()
ledge = pygame.image.load('art/Tile_Ledge.png').convert_alpha()
dashcrystal = pygame.image.load('art/Tile_Dashcrystal.png').convert_alpha()
dashcrystal_used = pygame.image.load('art/Tile_Dashcrystal_Used.png').convert_alpha()
maddy = pygame.image.load('art/Maddy_Body.png').convert_alpha()
maddy_tired_red = pygame.image.load('art/Maddy_Body_Flashred.png').convert_alpha()
maddy_tired_white = pygame.image.load('art/Maddy_Body_White.png').convert_alpha()
maddy_hair_red = pygame.image.load('art/Maddy_Hair_Red.png').convert_alpha()
maddy_hair_blue = pygame.image.load('art/Maddy_Hair_Blue.png').convert_alpha()
tilesize = block.get_height()
gamemap = map_config

#Movement parameters
maxv_x = movement_config[0]
maxv_y = movement_config[1]

#Gravity parameters
max_fall = gravity_config[0]
gravity = (maxv_y ** 2) / (6 * tilesize)
prefall_gravity = gravity_config[1] * gravity
postfall_gravity = gravity_config[2] * gravity

#Jumping parameters
jumpv = jumping_config[0] * maxv_y
walljump_max = jumping_config[1]
walljumpextend_max = jumping_config[2]

#Climbing parameters
stamina_max = climbing_config[0]
tired_limit = climbing_config[1]
grabbing_stamina = climbing_config[2]
climbingup_stamina = climbing_config[3]
climbingup_v = climbing_config[4]
climbingdown_v = climbing_config[5]

#Dash parameters
dashbuffer_time = dashing_config[0]
dash_time = dashing_config[1]
dash_speed = dashing_config[2]
diagonaldash_speed = mth.sqrt(dash_speed)
postdash_yvelocity = dashing_config[3]

#Crystal parameters
crystal_time = crystal_config[0]
boblimit = crystal_config[1]
bobrate = crystal_config[2]

#Level parameters
level_startpos = level_config[0]
level_endpos = level_config[1]
spikeson = level_config[2]
yoffset = level_config[3]

class CelesteEnvironment:

    #Initializes the CelesteEnvironment class
    def __init__(self):

        #Setup
        pygame.init()
        pygame.font.init()
        self.screen = pygame.Surface(gamedims)

        #Time
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.timer = 0
        self.timeoffset = 0
        self.besttime = 0

        #Font
        self.timerfont = pygame.font.SysFont(myfont[0], myfont[1])
        self.timertext = self.timerfont.render("", False, "white")
        self.deathfont = pygame.font.SysFont(myfont[0], myfont[1])
        self.deathtext = self.deathfont.render("", False, "white")

        #Coordinates
        self.x = 0
        self.y = 0

        #Madeline's hitbox
        self.maddy_rect = pygame.Rect(level_startpos[0], level_startpos[1], maddy.get_width(), maddy.get_height())
        
        #Madeline's true position
        self.maddy_pos = [self.maddy_rect.x, self.maddy_rect.y]

        #Movement
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
        self.walljump_pos = 0
        self.walljump_distance = walljump_max

        #Climbing
        self.istired = False
        self.cangrab = True
        self.isclimbingup = False
        self.isgrabbing = False
        self.stamina = stamina_max
        self.flashingcounter = 0

        #Dashing
        self.dashbuffer = dashbuffer_time
        self.dashcountdown = False
        self.hasdash = True
        self.isdashing = False
        self.dashdirection = ""

        #Dash crystal
        self.dashtimer = dash_time
        self.crystalused = False
        self.crystaltimer = crystal_time

        #Directional input
        self.isfacing = ""
        self.islooking = ""

        #Death
        self.isdead = False
        self.deathcount = 0
        
        #Collisions
        self.againstbottom = False
        self.tilerects = []
        self.spikerects = []
        self.ledgerects = []
        self.crystalrects = []
        self.collisiontypes = {'TOP': False, 'BOTTOM': False, 'RIGHT': False, 'LEFT': False}
        
    #Updates game
    def step(self, action):
        if self.isdead:
            self.ondeath()
        self.maddy_update(action)
        self.get_playeraction(action)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 return True
            if agent_config[0] == "HUMAN":
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
            elif agent_config[0] == "AI":
                if action == 4 or action == 5 or action == 6:
                    self.jump()
                if action == 3 or action == 7 or action == 8 or action == 9 or action == 10 or action == 13 or action == 14 or action == 15 or action == 16:
                    self.dashcountdown = True
                if action == 1 or action == 6 or action == 8 or action == 14 or action == 16:
                    self.movingright = True
                else:
                    self.isfacing = "RIGHT"
                    self.movingright = False
                if action == 0 or action == 5 or action == 7 or action == 13 or action == 15:
                    self.movingleft = True
                else:
                    self.isfacing = "LEFT"
                    self.movingleft = False
                if action != 2 and action != 11 and action != 12:
                    self.isgrabbing = False 
        self.dt = self.clock.tick_busy_loop(fps) / 1000
        self.timer = (pygame.time.get_ticks() / 1000) - self.timeoffset
        if agent_config[0] == "HUMAN":
            return False
        elif agent_config[0] == "AI":
            observations = self._get_obs()
            return observations, 0, False, {}
            
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
        self.check_reachedgoal()

    #Checks if Madeline reached the goal
    def check_reachedgoal(self):
        if self.maddy_pos[0] >= gamedims[0] - maddy.get_width():
            self.reset()

    #Resets Madeline's position on death
    def ondeath(self):
        self.deathcount += 1
        self.maddy_pos[0] = level_startpos[0]
        self.maddy_pos[1] = level_startpos[1]
        self.maddy_rect.x = self.maddy_pos[0]
        self.maddy_rect.y = self.maddy_pos[1]
        self.isdead = False

    #Refreshes dash crystals
    def update_crystal(self):
        if self.crystalused:
            self.crystaltimer -= self.dt
            if self.crystaltimer <= 0:
                self.crystalused = False
                self.crystaltimer = crystal_time

    #Checks if a jump is past its peak
    def check_jump(self):
        self.check_walljump()
        if self.maddy_yvelocity > 0:
            self.pastjumppeak = True
        else:
            self.pastjumppeak = False

    #Checks if a walljump is done
    def check_walljump(self):
        jumpdistance = self.walljump_pos - self.maddy_pos[0]
        if (jumpdistance >= self.walljump_distance) or (jumpdistance <= -self.walljump_distance):
            self.lockedmovement = [False, ""]
            self.walljump_distance = walljump_max

    #Checks if Madeline is dashing
    def check_dash(self, action):
        if self.dashcountdown:
            self.dashbuffer -= 1
            if self.dashbuffer == 0:
                self.move_dash(action)
                self.dashbuffer = dashbuffer_time
                self.dashcountdown = False
        if self.isdashing and self.dashtimer > 0:
            self.dash()
            self.dashtimer -= self.dt
        elif self.isdashing:
            self.dashtimer = dash_time
            self.isdashing = False
            if self.maddy_yvelocity < 0:
                self.maddy_yvelocity = postdash_yvelocity
            self.maddy_xvelocity = 0

    #Checks if Madeline is in the air
    def check_fallstate(self):
        if self.againstbottom:
            self.inair = False
            self.stamina = stamina_max
            self.istired = False
            self.cangrab = True
            if not self.isdashing:
                self.hasdash = True
        elif not self.isgrabbing and not self.isdashing:
            self.add_gravity()
            self.inair = True

    #Updates stamina
    def update_stamina(self):
        if self.isclimbingup:
            self.stamina -= self.dt * climbingup_stamina
        elif self.isgrabbing:
            self.stamina -= self.dt * grabbing_stamina
        if self.stamina < 0:
            self.stamina = 0
        if self.stamina <= tired_limit:
            self.istired = True
        if self.stamina == 0:
            self.isgrabbing = False
            self.cangrab = False
            self.isclimbingup = False
    
    #Implements gravity
    def add_gravity(self):
        if self.pastjumppeak:
            self.maddy_yvelocity += prefall_gravity * self.dt 
        else:
            self.maddy_yvelocity += postfall_gravity * self.dt
        if self.maddy_yvelocity > max_fall:
            self.maddy_yvelocity = max_fall

    #Crystal mechanics
    def check_crystal(self):
        if not self.crystalused:
            if not self.hasdash:
                self.hasdash = True
                self.stamina = stamina_max
            elif self.istired:
                self.stamina = stamina_max
            self.istired = False
            self.crystalused = True

    #Jump mechanics
    def jump(self):
        if not self.isgrabbing:
            if not self.inair:
                self.maddy_yvelocity = 0
                self.maddy_yvelocity -= jumpv
            elif self.againstwall[0]:
                self.walljump_pos = self.maddy_pos[0]
                self.lockedmovement[0] = True
                self.maddy_yvelocity = 0
                self.maddy_yvelocity -= jumpv
                if self.againstwall[1] == "RIGHT":
                    self.lockedmovement[1] = "LEFT"
                elif self.againstwall[1] == "LEFT":
                    self.lockedmovement[1] = "RIGHT"

    #Dash mechanics
    def dash(self):
        if self.dashdirection == "RIGHT":
            self.maddy_xvelocity = dash_speed
            self.maddy_yvelocity = 0
        elif self.dashdirection == "LEFT":
            self.maddy_xvelocity = -dash_speed
            self.maddy_yvelocity = 0
        elif self.dashdirection == "UP":
            self.maddy_xvelocity = 0
            self.maddy_yvelocity = -dash_speed
        elif self.dashdirection == "DOWN":
            self.maddy_xvelocity = 0
            self.maddy_yvelocity = dash_speed
        elif self.dashdirection == "UPRIGHT":
            self.maddy_xvelocity = diagonaldash_speed
            self.maddy_yvelocity = -diagonaldash_speed
        elif self.dashdirection == "DOWNRIGHT":
            self.maddy_xvelocity = diagonaldash_speed
            self.maddy_yvelocity = diagonaldash_speed
        elif self.dashdirection == "UPLEFT":
            self.maddy_xvelocity = -diagonaldash_speed
            self.maddy_yvelocity = -diagonaldash_speed
        elif self.dashdirection == "DOWNLEFT":
            self.maddy_xvelocity = -diagonaldash_speed
            self.maddy_yvelocity = diagonaldash_speed

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

    #Checks if Madeline is colling with blocks
    def collision(self):
        collisionlist = []
        for tile in self.tilerects:
            if pygame.Rect.colliderect(self.maddy_rect, tile):
                collisionlist.append(tile)
        return collisionlist

    #Checks if Madeline is colliding with spikes
    def spike_collision(self):
        for tile_rect in self.spikerects:
            if tile_rect.colliderect(self.maddy_rect):
                if spikeson:
                    self.isdead = True

    #Checks if Madeline is colliding with ledges
    def ledge_collision(self):
        for ledge_rect in self.ledgerects:
            if ledge_rect.colliderect(self.maddy_rect) and self.maddy_yvelocity > 0:
                self.maddy_rect.bottom = self.maddy_pos[1] = ledge_rect.top
                self.maddy_pos[1] -= maddy.get_height()
                self.collisiontypes['BOTTOM'] = True

    #Checks if Madeline is colliding with a dash crystal
    def crystal_collision(self):
        for tile_rect in self.crystalrects:
            if tile_rect.colliderect(self.maddy_rect):
                self.check_crystal()

    #Checks if Madeline is against the wall
    def check_againstwall(self):
        isagainstright = False
        isagainstleft = False
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

    #Checks if Madeline is on top of a block
    def check_againstbottom(self):
        isagainstbottom = False
        for tile in self.tilerects:   
            self.maddy_rect.y += 1
            if pygame.Rect.colliderect(self.maddy_rect, tile):
                isagainstbottom = True
            self.maddy_rect.y -= 1
        for tile in self.ledgerects:   
            self.maddy_rect.y += 1
            if pygame.Rect.colliderect(self.maddy_rect, tile) and self.maddy_yvelocity > 0 and self.maddy_pos[1] + maddy.get_height() <= tile.top:
                isagainstbottom = True
            self.maddy_rect.y -= 1
        if isagainstbottom:
            self.againstbottom = True
        else:
            self.againstbottom = False

    #Implements collisions
    def move_collision(self):
        self.collisiontypes = {'TOP': False, 'BOTTOM': False, 'RIGHT': False, 'LEFT': False}
        self.maddy_rect.x += self.maddy_xvelocity
        self.maddy_pos[0] += self.maddy_xvelocity
        collisions = self.collision()
        for tile in collisions:
            if self.maddy_xvelocity > 0:
                if self.maddy_pos[0] + maddy.get_width() - tile.left <= 2.5 or self.isdashing:
                    self.maddy_rect.right = self.maddy_pos[0] = tile.left
                    self.maddy_pos[0] -= maddy.get_width()
                    self.collisiontypes['RIGHT'] = True
            elif self.maddy_xvelocity < 0:
                if tile.right - self.maddy_pos[0] <= 2.5 or self.isdashing:
                    self.maddy_rect.left = self.maddy_pos[0] = tile.right
                    self.collisiontypes['LEFT'] = True
        self.maddy_rect.y += self.maddy_yvelocity
        self.maddy_pos[1] += self.maddy_yvelocity
        collisions = self.collision()
        for tile in collisions:
            if self.maddy_yvelocity > 0:
                self.maddy_rect.bottom = self.maddy_pos[1] = tile.top
                self.maddy_pos[1] -= maddy.get_height()
                self.collisiontypes['BOTTOM'] = True
            elif self.maddy_yvelocity < 0:
                self.maddy_rect.top = self.maddy_pos[1] = tile.bottom
                self.collisiontypes['TOP'] = True
                self.maddy_yvelocity = 0
        if self.maddy_pos[0] <= 0:
            self.maddy_rect.x = self.maddy_pos[0] = 0
        elif self.maddy_pos[0] >= gamedims[0] - maddy.get_width():
            self.maddy_rect.x = self.maddy_pos[0] = gamedims[0] - maddy.get_width()
        if self.maddy_pos[1] <= 0 - 2 * tilesize:
            self.maddy_rect.y = self.maddy_pos[1] = 0 - 2 * tilesize
        self.spike_collision()
        self.ledge_collision()
        self.crystal_collision()
        self.check_againstwall()
        self.check_againstbottom()

    #Renders all visuals
    def render(self):
        self.screen.fill(screencolor)
        self.render_maddy()
        self.render_gamemap()
        self.render_timer()
        self.render_deathcount()
        surf = pygame.transform.scale(self.screen, screendims)
        dis.blit(surf, (0, 0))
        pygame.display.flip()

    #Renders Madeline
    def render_maddy(self):
        if self.istired:
            if self.flashingcounter == 0:
                self.screen.blit(maddy_tired_white, (self.maddy_pos[0], self.maddy_pos[1]))
                self.flashingcounter += 1
            else:
                self.screen.blit(maddy_tired_red, (self.maddy_pos[0], self.maddy_pos[1]))
                self.flashingcounter -= 1
        else:
            self.screen.blit(maddy, (self.maddy_pos[0], self.maddy_pos[1]))
        if self.hasdash:
            self.screen.blit(maddy_hair_red, (self.maddy_pos[0], self.maddy_pos[1] - maddy_hair_red.get_height()))
        else:
            self.screen.blit(maddy_hair_blue, (self.maddy_pos[0], self.maddy_pos[1] - maddy_hair_blue.get_height()))

    #Renders the game map
    def render_gamemap(self):
        self.y = yoffset
        self.tilerects = []
        self.spikerects = []
        self.ledgerects = []
        self.crystalrects = []
        bob_height = boblimit
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
                    bob_offset = bob_height * mth.sin(mth.radians(pygame.time.get_ticks() * bobrate)) 
                    if not self.crystalused:
                        self.screen.blit(dashcrystal, (self.x*tilesize, self.y*tilesize + bob_offset))
                    else:
                        self.screen.blit(dashcrystal_used, (self.x*tilesize, self.y*tilesize + bob_offset))               
                if tile == '2':
                    self.spikerects.append(pygame.Rect(self.x*tilesize + 1, self.y*tilesize + 5, spikes.get_width() - 2, spikes.get_height() - 5))
                elif tile == '3':
                    self.ledgerects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, ledge.get_width(), ledge.get_height() - 7))
                elif tile == '4':
                    self.crystalrects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, dashcrystal.get_width(), dashcrystal.get_height()))
                elif tile != '0':
                    self.tilerects.append(pygame.Rect(self.x*tilesize, self.y*tilesize, block.get_width(), block.get_height()))
                self.x += 1            
            self.y += 1

    #Renders in game timer
    def render_timer(self):
        self.timertext = self.timerfont.render(str(round(self.timer, 2)), False, "white")
        self.screen.blit(self.timertext, (gamedims[0] - tilesize * 7, tilesize / 2))

    #Renders death count
    def render_deathcount(self):
        self.deathtext = self.deathfont.render(("Deaths: " + str(self.deathcount)), False, "white")
        self.screen.blit(self.deathtext, (gamedims[0] - tilesize * 7, tilesize * 2))

    #Performs player actions
    def get_playeraction(self, action):
        self.move_climb(action)
        self.move_leftright()
        self.move_look(action)

    #Climbing movement
    def move_climb(self, action):
        if agent_config[0] == "HUMAN":
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
                        self.maddy_yvelocity = climbingup_v
                        self.isclimbingup = True
                    elif action[pygame.K_DOWN]:
                        self.maddy_yvelocity = climbingdown_v
                        self.isclimbingup = False
                    else:
                        self.maddy_yvelocity = 0
                        self.isclimbingup = False
                else:
                    self.maddy_yvelocity = 0
            else:
                self.isclimbingup = False
        elif agent_config[0] == "AI":
            if action == 2 or action == 11 or action == 12:
                if self.cangrab:
                    if self.collisiontypes['LEFT'] or self.collisiontypes['RIGHT']:
                        self.isgrabbing = True
                    else:
                        self.isgrabbing = False
                        if self.istired:
                            self.cangrab = False
            if self.isgrabbing:
                if action == 11:
                    self.maddy_yvelocity = climbingup_v
                    self.isclimbingup = True
                elif action == 12:
                    self.maddy_yvelocity = climbingdown_v
                    self.isclimbingup = False
                else:
                    self.maddy_yvelocity = 0
                    self.isclimbingup = False
            else:
                self.isclimbingup = False


    #Moving left/right
    def move_leftright(self):
        if not self.isdashing and not self.isgrabbing:
            if not(self.movingleft and self.movingright):
                if self.lockedmovement[0]:
                    if self.lockedmovement[1] == "RIGHT":
                        self.maddy_xvelocity = maxv_x
                        if self.movingleft and self.walljump_pos == self.maddy_pos[0]:
                            self.walljump_distance = walljumpextend_max
                    elif self.lockedmovement[1] == "LEFT":
                        self.maddy_xvelocity = -maxv_x
                        if self.movingright and self.walljump_pos == self.maddy_pos[0]:
                            self.walljump_distance = walljumpextend_max
                elif self.movingright:
                    self.maddy_xvelocity = maxv_x
                elif self.movingleft:
                    self.maddy_xvelocity = -maxv_x
                else:
                    self.maddy_xvelocity = 0
            else:
                self.isfacing = "False"
                self.maddy_xvelocity = 0

    #Looking up/down
    def move_look(self, action):
        if agent_config[0] == "HUMAN":
            if not(action[pygame.K_UP] and action[pygame.K_DOWN]):
                if action[pygame.K_UP]:
                    self.islooking = "UP"
                elif action[pygame.K_DOWN]:
                    self.islooking = "DOWN"
                else:
                    self.islooking = "False"
        elif agent_config[0] == "AI":
            if action == 9 or action == 11 or action == 13 or action == 14:
                self.islooking = "UP"
            elif action == 10 or action == 12 or action == 15 or action == 16:
                self.islooking = "DOWN"
            else:
                self.islooking = "False" 

    #Dashing movement
    def move_dash(self, action):
        directions = []
        if agent_config[0] == "HUMAN":
            if action[pygame.K_RIGHT]:
                directions.append("RIGHT")
            if action[pygame.K_LEFT]:
                directions.append("LEFT")
            if action[pygame.K_UP]:
                directions.append("UP")
            if action[pygame.K_DOWN]:
                directions.append("DOWN")
        elif agent_config[0] == "AI":
            if action == 1 or action == 6 or action == 8 or action == 14 or action == 16:
                directions.append("RIGHT")
            if action == 0 or action == 5 or action == 7 or action == 13 or action == 15:
                directions.append("LEFT")
            if action == 9 or action == 11 or action == 13 or action == 14:
                directions.append("UP")
            elif action == 10 or action == 12 or action == 15 or action == 16:
                directions.append("DOWN")
        self.dash_direction(directions)

    #Adds the best time to a text file
    def add_best(self):
        self.besttime = self.timer
        f = open('best_time.txt', 'r').read()
        if f.strip() == '' or self.besttime < float(f):
            f = open('best_time.txt', 'w')
            f.write(str(round(self.besttime, 2)))
            f.close()

    #Resets the game
    def reset(self):

        #Time
        self.timeoffset += self.timer
        self.add_best()
        self.timer = 0
    
        #Madeline's true position
        self.maddy_pos[0] = level_startpos[0]
        self.maddy_pos[1] = level_startpos[1]
        self.maddy_rect.x = self.maddy_pos[0]
        self.maddy_rect.y = self.maddy_pos[1]

        #Movement
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
        self.walljump_pos = 0
        self.walljump_distance = walljump_max

        #Climbing
        self.istired = False
        self.cangrab = True
        self.isclimbingup = False
        self.isgrabbing = False
        self.stamina = stamina_max
        self.flashingcounter = 0

        #Dashing
        self.dashbuffer = dashbuffer_time
        self.dashcountdown = False
        self.hasdash = True
        self.isdashing = False
        self.dashdirection = ""

        #Dash crystal
        self.dashtimer = dash_time
        self.crystalused = False
        self.crystaltimer = crystal_time

        #Directional input
        self.isfacing = ""
        self.islooking = ""

        #Death
        self.isdead = False
        self.deathcount = 0
        
        #Collisions
        self.againstbottom = False
        self.tilerects = []
        self.spikerects = []
        self.ledgerects = []
        self.crystalrects = []
        self.collisiontypes = {'TOP': False, 'BOTTOM': False, 'RIGHT': False, 'LEFT': False}
 
        if agent_config[0] == "AI":
            return self._get_obs()

    #Gets observation
    def _get_obs(self):
        return {
            'maddy_x': np.array([self.maddy_pos[0]]),
            'maddy_y': np.array([self.maddy_pos[1]]),
            'maddy_x_velocity': np.array([self.maddy_xvelocity]),
            'maddy_y_velocity': np.array([self.maddy_yvelocity]),
            'dist2goal': np.array([mth.sqrt((level_endpos[0] - self.maddy_pos[0]) ** 2 + (level_endpos[1] - self.maddy_pos[1]) ** 2)])
        }

    #Returns player input
    @staticmethod
    def get_playerinput():
        return pygame.key.get_pressed()

    #Quits the game
    @staticmethod
    def close():
        pygame.quit()
