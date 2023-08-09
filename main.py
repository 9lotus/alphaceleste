"""
Author : Rori Wu, Zenia Haroon

Date : 7/27/23 - TBD

Description: Runs the Celeste program
"""
import stable_baselines3 as sb3
from stable_baselines3.common.env_checker import check_env

from celeste import CelesteEnvironment

Celeste = CelesteEnvironment()

# if human playing, this loop
terminated = False
while not terminated:
    action = Celeste.get_playerinput()
    terminated = Celeste.step(action)
    Celeste.render()

'''
check_env(Celeste)
 # Set up model
model = sb3.PPO("MultiInputPolicy", Celeste, verbose=1)
model.learn(total_timesteps=250000)
model.save("alphaceleste")

del model
#Load and evaluate agent
model = sb3.PPO.load("alphaceleste")
obs = Celeste.reset()

# if ai playing, this loop
done = False
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, info = Celeste.step(action)
    Celeste.render()

'''
Celeste.close()