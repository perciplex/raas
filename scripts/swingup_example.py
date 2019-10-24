import path_utils
import gym
import raas_envs
import numpy as np
from time import sleep


def get_action(state):

    x, y, theta_dot = state

    stay_up_thresh = -0.8
    prop_torque = 0.1
    max_torque = 2.0
    turnaround_speed_thresh = 0.2

    if x <= stay_up_thresh:
        if y <= 0:
            torque = -prop_torque * max_torque
        else:
            torque = prop_torque * max_torque
    else:
        if y <= 0:
            if theta_dot >= 0:
                torque = -max_torque
            else:
                torque = max_torque
        else:
            if theta_dot >= 0:
                torque = max_torque
            else:
                torque = -max_torque

    return np.array([torque])


# natural freq: omega = 5.2 ==> f = 5.2/5.3 = 0.82

print("Creating gym object...")
# Creates and returns Pendulum env object
env_pend = gym.make("pendulum-v0")

N_steps = 300
time_incr = 0.05
w = 5.4
s = env_pend.reset()
for t in range(N_steps):

    sleep(time_incr)

    print(f"Step {t}")
    # action = np.array([2.0*np.sin(w*t*time_incr)])
    action = get_action(s)
    print("\tAction: {}".format(action))
    s_next, r, done, _ = env_pend.step(action)
    print("\tState: {}, reward: {}, state: {}".format(s_next, r, env_pend.state))

    s = s_next


print("\nDone!")


#
