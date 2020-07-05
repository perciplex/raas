import gym

import time
import numpy as np
import scipy.linalg as linalg

lqr = linalg.solve_continuous_are

g = 9.81
m = 0.05  # pendulum mass = 40 g
l = 0.51  # pendulum length = 50 cm
I = (1.0 / 3.0) * m * l ** 2  # moment of inertia


def E(x):  # energy
    theta, theta_dot = x
    return (I * theta_dot ** 2 / 2) + (np.cos(theta) * l * m * g / 2)


Ed = E([0, 0]) + 0.002


def u(x):
    theta, theta_dot = x
    return 1.0 * (E(x) - Ed) * theta_dot


A = np.array([[0, 1], [m * g * l / (2 * I), 0]])

B = np.array([0, 1.0 / I]).reshape((2, 1))
Q = np.diag([10.0, 3.0])
R = np.array([[300.0]])

P = lqr(A, B, Q, R)
Rinv = np.linalg.inv(R)
K = np.dot(Rinv, np.dot(B.T, P))
print(K)


def ulqr(x):
    return -np.dot(K, x) / (0.25 * 0.25 * g / 100.0)


env = gym.make("raaspendulum-v0")
env.reset()

N_steps = 1000

observation = env.reset()
observation, reward, done, info = env.step([2])
time.sleep(1)

for t in range(N_steps):
    time.sleep(0.01)
    print(f"Step {t}")
    observation = np.arctan2(observation[1], observation[0]), observation[2]

    if np.cos(observation[0]) > 0.94:  # balance
        print("🚨 linear control 🚨")
        action = ulqr(observation)[0]
    else:
        action = -5 * u(observation)  # swing up

    print(action, observation, E(observation) - Ed)
    # env.render()
    observation, reward, done, info = env.step([action])


print("\nDone!")
