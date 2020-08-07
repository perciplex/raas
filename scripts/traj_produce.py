import gym
import gym_raas
import numpy as np
import time
import matplotlib.pyplot as plt
import argparse
import calibrate_pend_resonance
import socket
import pprint
import json


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
        w = 5.0
        if HARDWARE:
            name = socket.gethostname()
        else:
            name = "simulation_raas"

    print("Set up!")
    print(f"\nUsing OpenAI pendulum: {use_openai}")
    print(f"\n\nRUNNING IN HARDWARE MODE: {HARDWARE}\n\n")

    calibrate_pend_resonance.find_bottom_initial_cond(env, HARDWARE)

    n_steps = 200
    obs = []
    DT = 0.05
    max_torque = 1.0

    action_obs, _ = calibrate_pend_resonance.get_resonant_trajectory(
        env, w, max_torque, n_steps, HARDWARE, use_rand_max_torque=True
    )

    return action_obs


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    # False unless you give the openai flag
    parser.add_argument(
        "--openai", action="store_true", help="Use the openai pendulum env instead"
    )
    args = parser.parse_args()

    traj = get_traj(args.openai)
    print("\n\nAction obs list:\n")

    print("\n")
    print("\n")
    print(json.dumps(traj, indent=4))
    print("\n")

    exit()

    x = [t["s"][0] for t in traj]
    y = [t["s"][1] for t in traj]
    plt.plot(y, x)
    plt.show()
