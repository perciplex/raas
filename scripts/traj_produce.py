import gym
import gym_raas
import numpy as np
import time


def get_traj():
    print("Setting up env...")
    env = gym.make("raaspendulum-v0")
    # env = gym.make("Pendulum-v0")
    print("Set up!")
    env.reset()

    n_steps = 100
    obs = []
    # Use w = 4 for openAI pend, use w = 5.5 for our pend sim,
    # w = 4.0
    SIMULATION = True
    time_incr = 0.05
    max_torque = 0.3

    print("\nResetting env...")
    found_init = False
    # print(f'Original env.state is {env.state}')
    while not found_init:
        env.reset()
        env.step([0.0])
        th, thdot = env.state
        s = env.state
        if abs(th) > 3.1 and abs(thdot) < 0.05:
            print("found good init!")
            print(env.state)
            found_init = True

    max_ep_amp = None
    action_obs = []
    for t in range(n_steps):
        if np.sin(w * t * time_incr) > 0:
            mult = 1.0
        else:
            mult = -1.0
        action = 2.0 * np.sin(w * t * time_incr)
        # action = mult * max_torque
        o, reward, _, _ = env.step([action])
        x, y, thdot = o
        theta = np.arctan2(y, x)
        s_next = [theta, thdot]
        # [action, theta, np.sin(theta + np.pi), thdot]
        action_obs.append({"s": s, "u": action, "s_next": s_next})
        s = s_next

    return action_obs


if __name__ == "__main__":

    print(get_traj())
