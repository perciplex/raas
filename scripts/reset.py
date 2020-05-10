import gym
import gym_raas

from time import sleep
import numpy as np

settle_time = 30.0


def reset_pendulum():
    # create env
    env = gym.make("raaspendulum-v0")
    env.reset()

    sleep(1.0)
    print("Giving kick to make sure pendulum still isnt standing up...")
    _, _, _, _ = env.step([2])  # start with an initial impulse
    print("Done, sleeping for {} seconds to let it settle...".format(settle_time))
    sleep(settle_time)
    _, _, _, _ = env.step([0])

    print("Done!")
