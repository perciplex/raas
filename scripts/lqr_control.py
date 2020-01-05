import gym
from time import sleep

import time
import numpy as np
import scipy.linalg as linalg
lqr = linalg.solve_continuous_are

g = 9.81
m = 0.04 # pendulum mass = 40 g
l = 0.5 # pendulum length = 50 cm
I = (1./3.) * m * l**2 # moment of inertia

def E(x): # energy
    cos_theta, sin_theta, theta_dot = x
    return (I * theta_dot**2 / 2) - (cos_theta * l * m * g / 2)

Ed = E([1,0,0])

def u(x):
    cos_theta, sin_theta, theta_dot = x
    return  1.0 * (E(x)-Ed) * theta_dot

A = np.array([
    [0,0,0],
    [0,0,0],
    [0, m * g * l / (2 * I), 0]
	])

B = np.array([0,0,l * m / (2 * I)]).reshape((3,1))
Q = np.diag([1,0.,.5])
R = np.array([[0.01]])

P = lqr(A,B,Q,R)
Rinv = np.linalg.inv(R)
K = np.dot(Rinv,np.dot(B.T, P))
print(K)
def ulqr(x):
	return -np.dot(K, x)



env = gym.make('Pendulum-v0')
env.reset()

N_steps = 300

observation = env.reset()

for t in range(N_steps):
    print(f"Step {t}")

    if  abs(E(observation)-Ed) < 0.05 and np.cos(observation[2]) < -0.9 and abs(command_speed)<4: # balance
        print("linear control")
        action = 1.0 * ulqr(observation)[0]
    else:
        action = 0.5*(u(observation)/0.15 - 10.0 * observation[0] -  1.0 * observation[1]) # swing up
    
    
    env.render()
    observation, reward, done, info = env.step(action)


print("\nDone!")
