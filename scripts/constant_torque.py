import path_utils
import raas_gym
import numpy as np
import time


print('Creating gym object...')
# Creates and returns Pendulum env object
env_pend = raas_gym.make('Pendulum-v0')

print('Setting to constant torque')
action = np.array([0.5])

s_next, r, done, _ = env_pend.step(action)

print('Sleeping...')
time.sleep(3)

print('\nDone!')


#
