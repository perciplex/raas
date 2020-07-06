import gym
import numpy as np
from scipy import linalg as linalg

lqr = linalg.solve_continuous_are

g = 10.0
m = 1.0  # 0.04 # pendulum mass = 40 g
l = 1.0  # 0.5 # pendulum length = 50 cm
I = (1.0 / 3.0) * m * l ** 2  # moment of inertia


def E(x):  # energy
    theta, theta_dot = x
    return (I * theta_dot ** 2 / 2) + (np.cos(theta) * l * m * g / 2)


Ed = E([0, 0])


def u(x):
    theta, theta_dot = x
    return 1.0 * (E(x) - Ed) * theta_dot


A = np.array([[0, 1], [-m * g * l / (2 * I), 0]])

B = np.array([0, l * m / (2 * I)]).reshape((2, 1))
Q = np.diag([10.0, 0.5])
R = np.array([[0.01]])

P = lqr(A, B, Q, R)
Rinv = np.linalg.inv(R)
K = np.dot(Rinv, np.dot(B.T, P))
print(K)


def ulqr(x):
    return -np.dot(K, x)


env = gym.make("Pendulum-v0")
env.reset()

N_steps = 300

observation = env.reset()

for t in range(N_steps):
    print(f"Step {t}")
    observation = np.arctan2(observation[1], observation[0]), observation[2]

    if abs(E(observation) - Ed) < 1.0 and np.cos(observation[0]) > 0.9:  # balance
        print("linear control")
        action = 10.0 * ulqr(observation)[0]
    else:
        action = -0.5 * u(observation)  # swing up

    print(observation, E(observation) - Ed, np.cos(observation[0]))
    env.render()
    observation, reward, done, info = env.step([action])


print("\nDone!")
