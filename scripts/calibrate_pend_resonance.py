import gym
import gym_raas
import numpy as np
import time
import pprint


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


def get_resonant_trajectory(env, w, max_torque, n_steps, is_hardware):

    max_ep_amp = None
    action_obs = []
    o, _, _, _ = env.step([0.0])
    # x is np.cos(theta), where x=1 at the top and x=-1 at the bottom.
    x, y, thdot = o
    theta = np.arctan2(y, x)
    s = [theta, thdot]

    for t in range(n_steps):
        phase = np.sin(w * t * DT)
        if phase > 0:
            mult = 1.0
        else:
            mult = -1.0
        # action = max_torque * phase
        action = mult * max_torque
        o, _, _, _ = env.step([action])
        # x is np.cos(theta), where x=1 at the top and x=-1 at the bottom.
        x, y, thdot = o
        theta = np.arctan2(y, x)
        s_next = [theta, thdot]
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

    use_openai = False

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
    w_range = np.linspace(3, 7, 30)

    max_torque = 1.0

    n_steps = 200

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
