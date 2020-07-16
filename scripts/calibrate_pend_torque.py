import gym
import gym_raas
import numpy as np
import time

env = gym.make("raaspendulum-v0")
env.reset()
obs = []


N_steps = 400

torque_range = np.linspace(0, 2.0, 10)


try:
    for t in torque_range:

        observation, reward, done, info = env.step([torque])
        time.sleep(5.0)
        obs.append(observation)

except:
    print("Stopped!")


[print(o) for o in obs]

env.reset()
