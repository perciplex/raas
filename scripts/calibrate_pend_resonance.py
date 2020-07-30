import gym
import gym_raas
import numpy as np
import time
import pprint
import argparse

DT = 0.05


def find_bottom_initial_cond(env, is_hardware):

    print("\nFinding initial condition with pendulum at bottom...")
    found_init = False
    while not found_init:
        if is_hardware:
            time.sleep(1.0)
            print("Trying reset again now...")

        env.reset()
        env.step([0.0])  # So env.state is defined for hardware version
        th, thdot = env.state
        # We want it to be both at the bottom and stopped. I found that some
        # of the robots will never actually get to ~3.14, but most will relax
        # to > 3.0.
        if abs(th) > 3.0 and abs(thdot) < 0.05:
            print("Found good init!")
            print(env.state)
            found_init = True
        else:
            if is_hardware:
                print(
                    "Not settled yet, theta = {:.2f}, thetadot = {:.2f}".format(
                        th, thdot
                    )
                )


def get_resonant_trajectory(
    env, w, max_torque, n_steps, is_hardware, use_phase_torque=False, use_rand_max_torque=False,
):

    max_ep_amp = None
    action_obs = []
    o, _, _, _ = env.step([0.0])
    # x is np.cos(theta), where x=1 at the top and x=-1 at the bottom.
    x, y, thdot = o
    theta = np.arctan2(y, x)
    s = [x, y, thdot, theta]

    for t in range(n_steps):
        phase = np.sin(w * t * DT)
        if use_phase_torque:
            action = max_torque * phase
        else:
            if phase > 0:
                mult = 1.0
            else:
                mult = -1.0
            action = mult * max_torque

        if use_rand_max_torque:
            action *= (1 + 0.5*np.random.randn())

        o, _, _, _ = env.step([action])
        # x is np.cos(theta), where x=1 at the top and x=-1 at the bottom.
        x, y, thdot = o
        theta = np.arctan2(y, x)
        s_next = [x, y, thdot, theta]
        action_obs.append({"s": s, "u": action, "s_next": s_next})
        s = s_next

        if is_hardware:
            time.sleep(DT)

        if (max_ep_amp is None) or (x > max_ep_amp):
            max_ep_amp = x

    return action_obs, max_ep_amp


def get_max_amp(env, w, max_torque, n_steps, is_hardware):

    _, max_ep_amp = get_resonant_trajectory(
        env, w, max_torque, n_steps, is_hardware
    )

    return max_ep_amp


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--freq_start", type=float, default=3.0, help="The start freq to use")
    parser.add_argument("--freq_end", type=float, default=7.0, help="The end freq to use")
    parser.add_argument("--steps", type=int, default=30, help="The steps between the start and end freqs")

    parser.add_argument("--swing_steps", type=int, default=200, help="The number of steps to swing at each freq")
    parser.add_argument("--max_torque", type=int, default=1.0, help="The number of steps to swing at each freq")

    # False unless you give the openai flag
    parser.add_argument("--openai", action='store_true', help="Use the openai pendulum env instead")
    args = parser.parse_args()



    use_openai = args.openai

    print("Setting up env...")
    if use_openai:
        env = gym.make("Pendulum-v0")
        HARDWARE = False
        name = "simulation_openAI"
    else:
        env = gym.make("raaspendulum-v0")
        HARDWARE = env.hardware
        if HARDWARE:
            name = "HARDWARE"
        else:
            name = "simulation_raas"

    print("Set up!")
    print(f"\nUsing OpenAI pendulum: {use_openai}")
    print(f"\n\nRUNNING IN HARDWARE MODE: {HARDWARE}\n\n")

    # w_range = np.linspace(3, 4, 2)
    #w_range = np.linspace(3, 7, 30)
    w_range = np.linspace(args.freq_start, args.freq_end, args.steps)

    max_torque = args.max_torque

    n_steps = args.swing_steps

    max_amps = []

    for w in w_range:

        print("Running with freq = {:.2f} now".format(w))

        find_bottom_initial_cond(env, HARDWARE)

        max_amp = get_max_amp(env, w, max_torque, n_steps, HARDWARE)

        print("\nMax amplitude found: ", max_amp)
        max_amps.append(max_amp)

    print("\nFreqs:")
    print(w_range.tolist())

    print("\nMax amplitudes:")
    print(max_amps)

    d = {"name": name, "freqs": w_range.tolist(), "max_amps": max_amps}

    print("\n")
    pprint.pprint(d)
    print("\n")

    env.reset()
