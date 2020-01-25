import gym
import gym_raas

from time import sleep
import numpy as np

import zmq


settle_time = 15.0

def reset_pendulum():
    # create env
    env = gym.make('raaspendulum-v0')
    env.reset()

    sleep(1.0)
    print('Giving kick to make sure pendulum still isnt standing up...')
    _, _, _, _ = env.step([2]) # start with an initial impulse
    print('Done, sleeping for {} seconds to let it settle...'.format(settle_time))
    sleep(settle_time)

<<<<<<< HEAD
=======
    socket.connect("tcp://172.17.0.1:5555")

    socket.send_pyobj(("Reset", None))
    _ = socket.recv_pyobj()

>>>>>>> f72708ee057963ac364051efd8562ee18f7bb3d5
    print('Done!')
