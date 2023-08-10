import gymnasium as gym
from gymnasium import spaces
import numpy as np
from celeste import CelesteEnvironment
import math as mth
import yaml

#yaml configs
with open("./config/game_parameters.yaml", 'r') as stream:
    out = yaml.safe_load(stream)
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

level_startpos = level_config[0]
level_endpos = level_config[1]
screen_width = screen_config[1][0]
screen_height = screen_config[1][1]
print(screen_width)

class CelesteGymEnv(gym.Env):
    def __init__(self):
        self.env = CelesteEnvironment()
        self.action_space = gym.spaces.Discrete(8)  # Actions: 0 to 7 -- Zenia implements
        self.observation_space = spaces.Dict(
            {
                'maddy_x': spaces.Box(low=0, high=screen_width, shape=(1,), dtype = np.uint8),
                'maddy_y': spaces.Box(low=0, high=screen_height, shape=(1,), dtype = np.uint8),
                'maddy_x_velocity': spaces.Box(low=0, high=1.5, shape=(1,), dtype = float),
                'maddy_y_velocity': spaces.Box(low= 0, high=3.4, shape=(1,), dtype = float),
                'dist2goal': spaces.Box(low=0, high=(mth.sqrt((self.screen_width **2)+ (self.screen_height **2))), shape = (1,), dtype = float)
            }
        )
        self.done = False
        self.startpos = level_startpos
        self.endpos = level_endpos

    def step(self, action):
        obs, _, done, _ = self.env.step(action)
        agent_pos = self.env.maddy_pos
        distance_to_end = mth.sqrt((self.endpos[0] - agent_pos[0])**2 + (self.endpos[1] - agent_pos[1])**2)
        reward = 1.0 / (1.0 + distance_to_end)  # Higher reward for being closer to endpos -- Rori implements "checkpoints"

        self.done = self.env.maddy_pos[0] >= self.endpos[0]  # Check if the agent has reached the endpos

        return obs, reward, done, {}

    def reset(self):
        obs = self.env.reset()
        self.done = False
        return obs

    def render(self, mode='human'):
        self.env.render()

    def close(self):
        self.env.close()

# Create the Gym environment
env = CelesteGymEnv()

