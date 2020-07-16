import gym
import gym_raas
import numpy as np
import time

import calibrate_pend_resonance


def get_traj(use_openai):

    print("Setting up env...")
    if use_openai:
        env = gym.make("Pendulum-v0")
        HARDWARE = False
        name = "simulation_openAI"
        w = 4.0
    else:
        env = gym.make("raaspendulum-v0")
        HARDWARE = env.hardware
        w = 5.5
        if HARDWARE:
            name = "HARDWARE"
        else:
            name = "simulation_raas"

    print("Set up!")
    print(f"\nUsing OpenAI pendulum: {use_openai}")
    print(f"\n\nRUNNING IN HARDWARE MODE: {HARDWARE}\n\n")

    action_obs, _ = calibrate_pend_resonance.find_bottom_initial_cond(
        env, HARDWARE
    )

    n_steps = 200
    obs = []
    DT = 0.05
    max_torque = 1.0

    calibrate_pend_resonance.get_resonant_trajectory(
        env, w, max_torque, n_steps, HARDWARE
    )

    return action_obs


if __name__ == "__main__":

    print(get_traj())
