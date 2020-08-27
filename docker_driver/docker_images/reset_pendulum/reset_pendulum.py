from time import sleep

import gym
import gym_raas  # noqa

settle_time = 15.0

env = gym.make("raaspendulum-v0")
env.reset()

sleep(1.0)
print("Giving kick to make sure pendulum still isnt standing up...\n")
_, _, _, _ = env.step([2])  # start with an initial impulse
sleep(0.1)
_, _, _, _ = env.step([0])  # start with an initial impulse
print("Kicked! Sleeping for {} seconds to let it settle...\n".format(settle_time))
sleep(settle_time)

print("Done!")
