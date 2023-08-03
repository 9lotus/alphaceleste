"""
Author : Rori Wu, Zenia Haroon

Date : 7/27/23

Description: Runs the Celeste program
"""

from celeste import CelesteEnvironment

Celeste = CelesteEnvironment()
terminated = False
while not terminated:
    action = Celeste.get_playerinput()
    terminated = Celeste.step(action)
    Celeste.render()
Celeste.close()