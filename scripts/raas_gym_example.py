from time import sleep

import gym
import numpy as np

# natural freq: omega = 5.2 ==> f = 5.2/5.3 = 0.82

print("Creating gym object...")
# Creates and returns Pendulum env object
env_pend = gym.make("pendulum-v0")

N_steps = 300
time_incr = 0.05
w = 5.4
s = None
for t in range(N_steps):

    sleep(time_incr)

    print(f"Step {t}")
    action = np.array([2.0 * np.sin(w * t * time_incr)])
    print("\tAction: {}".format(action))
    s_next, r, done, _ = env_pend.step(action)
    print("\tState: {}, reward: {}".format(s_next, r))

    s = s_next


print("\nDone!")


#
