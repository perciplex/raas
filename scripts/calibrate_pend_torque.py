import gym
import gym_raas
import numpy as np
import time

print("Setting up env...")
env = gym.make("raaspendulum-v0")
print("Set up!")
env.reset()
obs = []

torque_range = np.linspace(0, 2.0, 10)


try:
    for t in torque_range:
        print("Running with torque = {:.2f} now".format(t))
        observation, reward, done, info = env.step([t])
        time.sleep(8.0)
        obs.append(observation)

except:
    print("Stopped!")


print("\nTorques:")
print(torque_range)

print("\nObservations:")
[print(o) for o in obs]

env.reset()
