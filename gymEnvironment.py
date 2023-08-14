"""
Author : Zenia Haroon, Rori Wu

Date : 8/10/23 - TBD

Description : Contains the gym environment to train the AI agent
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from celeste import CelesteEnvironment
import math as mth

level_endpos = (312,69)
level_startpos = (16, 156)
screen_height = 180
screen_width = 320
checkpoint_1 = [58, 72, 132, True]
checkpoint_2 = [46, 60, 76, True]
checkpoint_3 = [24, 38, 36, True]
checkpoint_4 = [128, 152, 55, True]
checkpoint_5 = [216, 224, 84, True]
checkpointslist = [checkpoint_1, checkpoint_2, checkpoint_3, checkpoint_4, checkpoint_5]

class CelesteGymEnv(gym.Env):
    def __init__(self, render_mode="human"):
        self.env = CelesteEnvironment()
        
        #Defining individual actions
        self.actions = ['left', 'right', 'z', 'x', 'c']

        #Defining action combos
        self.combinations = [
            ['c', 'left'], ['c', 'right'],
            ['x', 'left'], ['x', 'right'], ['x', 'up'], ['x', 'down'],
            ['z', 'up'], ['z', 'down'],
            ['x', 'up', 'left'], ['x', 'up', 'right'],
            ['x', 'down', 'left'], ['x', 'down', 'right']
        ]
        #Total num of actions
        self.num_actions = len(self.actions) + len(self.combinations)
        
        #Defining action space
        self.action_space = gym.spaces.Discrete(self.num_actions) 

        self.observation_space = spaces.Dict(
            {
                'maddy_x': spaces.Box(low=0, high=screen_width, shape=(1,), dtype = float),
                'maddy_y': spaces.Box(low=0, high=screen_height, shape=(1,), dtype = float),
                'maddy_x_velocity': spaces.Box(low=0, high=1.5, shape=(1,), dtype = float),
                'maddy_y_velocity': spaces.Box(low= 0, high=3.4, shape=(1,), dtype = float),
                'dist2goal': spaces.Box(low=0, high=(mth.sqrt((screen_width **2)+ (screen_height **2))), shape = (1,), dtype = float)
            }
        )
        self.render_mode = render_mode
        self.done = False
        self.startpos = level_startpos
        self.endpos = level_endpos

    def step(self, action): 
        obs, _, done, _ = self.env.step(action)
        agent_pos = self.env.maddy_pos
        death_status = self.env.isdead
        distance_to_end = mth.sqrt((self.endpos[0] - agent_pos[0])**2 + (self.endpos[1] - agent_pos[1])**2)
        reward = 1.0 / (1.0 + distance_to_end / 10)  # Higher reward for being closer to endpos
        for point in checkpointslist:
            if point[3]: # If checkpoint hasn't been reached yet
                if agent_pos[0] >= point[0] and agent_pos[0] <= point[1] and agent_pos[1] >= point[2]: #If player pos is within the checkpoint's range
                    point[3] = False
                    reward += 0.25
        if death_status == True:
            reward -= 0.1
        self.done = self.env.maddy_pos[0] >= self.endpos[0]  # Check if the agent has reached the endpos

        #Converting action index to actions
        if action < len(self.actions):
            chosen_action = self.actions[action]
        else:
            chosen_action = self.combinations[action - len(self.actions)]

        if self.render_mode == "human": self.render()

        return obs, reward, done, False, {}

    def reset(self, seed=None):
        obs = self.env.reset()
        self.done = False
        return obs, {}

    def render(self, mode='human'):
        self.env.render()

    def close(self):
        self.env.close()

# Create the Gym environment
env = CelesteGymEnv()

