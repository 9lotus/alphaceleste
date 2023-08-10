"""
Author : Rori Wu, Zenia Haroon

Date : 7/27/23 - TBD

Description: Runs the Celeste program
"""
import stable_baselines3 as sb3
from stable_baselines3.common.env_checker import check_env
import yaml

with open("./config/game_parameters.yaml", 'r') as stream:
    out = yaml.safe_load(stream)
agent_config = out['agent']

from celeste import CelesteEnvironment
from gymEnvironment import CelesteGymEnv

CelestePlayer = CelesteEnvironment()
CelesteAI = CelesteGymEnv()

check_env(CelesteAI)
 # Set up model
model = sb3.PPO("MultiInputPolicy", CelesteAI, verbose=1)
model.learn(total_timesteps=250000)
model.save("alphaceleste")

del model
# Load and evaluate agent
model = sb3.PPO.load("alphaceleste")
obs = CelesteAI.reset()

if agent_config[0] == "HUMAN":
    # if human playing, this loop
    done = False
    while not done:
        action = CelestePlayer.get_playerinput()
        done = CelestePlayer.step(action)
        CelestePlayer.render()
    CelestePlayer.close()
elif agent_config[0] == "AI":
    # if ai playing, this loop
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, info = CelesteAI.step(action)
        CelesteAI.render()
    CelesteAI.close()