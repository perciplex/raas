import numpy as np
from os import path
from gym import spaces

'''

Pendulum class. Continuous action space. Meant to recreate Pendulum-v0,
which is implemented here:

https://github.com/openai/gym/blob/master/gym/envs/classic_control/pendulum.py

Most of it is kept the same (reward structure, etc), except the part that has
to actually interface with the env.

'''

class Pendulum:

    def __init__(self, g=10.0):
        self.max_speed=8
        self.max_torque=2.
        self.dt=.05
        self.g = g
        self.viewer = None

        high = np.array([1., 1., self.max_speed])
        self.action_space = spaces.Box(low=-self.max_torque, high=self.max_torque, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-high, high=high, dtype=np.float32)

        #self.seed()
        # See comment in random() below about random initial conditions.

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self,u):
        th, thdot = self.state # th := theta

        g = self.g
        m = 1.
        l = 1.
        dt = self.dt

        '''
        u = np.clip(u, -self.max_torque, self.max_torque)[0]
        self.last_u = u # for rendering
        costs = angle_normalize(th)**2 + .1*thdot**2 + .001*(u**2)

        newthdot = thdot + (-3*g/(2*l) * np.sin(th + np.pi) + 3./(m*l**2)*u) * dt
        newth = th + newthdot*dt
        newthdot = np.clip(newthdot, -self.max_speed, self.max_speed) #pylint: disable=E1111

        self.state = np.array([newth, newthdot])
        return self._get_obs(), -costs, False, {}
        '''

        ### CALCULATE REWARD
        costs = angle_normalize(th)**2 + .1*thdot**2 + .001*(u**2)

        ### EXECUTE ACTION IN ROBOT
        ### GET NEXT STATE FROM MEASUREMENT
        ### update state
        ### RETURN:
        ### return self._get_obs(), -costs, False, {}


    def reset(self):
        # Currently, uses randomness for initial conditions. We could either
        # remove this aspect, or do something like create initial randomness by
        # doing a quick sequence of actions before starting the episode, that
        # would effectively start it in a random state.
        high = np.array([np.pi, 1])
        self.state = self.np_random.uniform(low=-high, high=high)
        self.last_u = None
        return self._get_obs()

    def _get_obs(self):
        '''
        This has to be replaced by some lower level raspi_robot.get_measurement()
        function!
        '''
        theta, thetadot = self.state
        return np.array([np.cos(theta), np.sin(theta), thetadot])

    def render(self, mode='human'):

        # Probably not necessary for now. Maybe interface with actual gym
        # display later?
        pass

    def close(self):
        # We'd probably want something to destroy the connection/etc to the
        # lower level robot object?
        pass

def angle_normalize(x):
    return (((x+np.pi) % (2*np.pi)) - np.pi)
