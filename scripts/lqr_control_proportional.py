import gym

from time import sleep
import numpy as np


g = 9.81  # earth's gravity
m = 0.05  # pendulum mass = 40 g
l = 0.51  # pendulum length = 50 cm
I = (1.0 / 3.0) * m * l ** 2  # moment of inertia of a rod


def E(theta, theta_dot):  # energy
    return (I * theta_dot ** 2 / 2) + (np.cos(theta) * l * m * g / 2)


target_energy = E(0, 0)  # energy of the pendulum in the up position with no speed


k_swingup = 5  # swing up magnitude constant
k_proportional = 15.0  # propirtional control constant

controller_handoff = (
    0.94  # threshold value of cos(theta) for swing up and proportional control
)


def proportional_torque(theta, theta_dot):  # calculate the proportional torque
    return -k_proportional * theta


def swing_up_torque(theta, theta_dot):  # calculate the swingup torque
    return -k_swingup * (E(theta, theta_dot) - target_energy) * theta_dot  #


n_steps = 1000  # set length of run

env = gym.make("raaspendulum-v0")  # initialize envoirment
env.reset()

observation, reward, done, info = env.step([2])  # start with an initial impulse
sleep(1)

for t in range(n_steps):  # main loop
    print(f"step {t} out of {n_steps}")

    sleep(0.01)  # match simulation rate

    theta = np.arctan2(observation[1], observation[0])  # calculate theta
    theta_dot = observation[2]

    if (
        np.cos(theta) > controller_handoff
    ):  # handoff between swing up control controller and proportional controller
        print("🚨  proportional control 🚨")
        action = proportional_torque(theta, theta_dot)  # proportional control
    else:
        action = swing_up_torque(theta, theta_dot)  # swing up

    print(
        f"""action {action}
theta {theta}
theta_dot {theta_dot}
energy_difference {E(theta, theta_dot) - target_energy}
        """
    )
    observation, reward, done, info = env.step([action])


env.reset()
print("done")
