import gym
import gym_raas
import numpy as np
import time

env = gym.make("raaspendulum-v0")
env.reset()
obs = []

torque_range = np.linspace(0, 2.0, 10)


try:
    for t in torque_range:
        print("Running with torque = {.2f} now".format(t))
        observation, reward, done, info = env.step([t])
        time.sleep(5.0)
        obs.append(observation)

except:
    print("Stopped!")


[print(o) for o in obs]

env.reset()
