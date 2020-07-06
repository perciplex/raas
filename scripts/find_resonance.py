from time import sleep

import numpy as np
import raas_gym

# natural freq: omega = 5.2 ==> f = 5.2/5.3 = 0.82

print("Creating gym object...")
# Creates and returns Pendulum env object
env_pend = raas_gym.make("Pendulum-v0")

N_steps = 300
time_incr = 0.05

w_range = np.linspace(4.2, 5.6, 12)
max_amps = []

for w in w_range:

    print(f"\nRunning with w = {w:.2f}")
    s = None

    max_ep_amp = None

    for t in range(N_steps):

        sleep(time_incr)

        action = np.array([2.0 * np.sin(w * t * time_incr)])
        s_next, r, done, _ = env_pend.step(action)

        if t % max(N_steps / 10, 1) == 0:
            print(f"Step {t}")
            print("\tAction: {}".format(action))
            print("\tState: {}, reward: {:.3f}".format(s_next, r))

        x, y, _ = s_next

        if (max_ep_amp is None) or (-x > max_ep_amp):
            max_ep_amp = -x

        s = s_next

    max_amps.append(max_ep_amp)
    print(f"\nMax episode amplitude = {max_ep_amp:.2f}")

    print("\nResetting...")
    s_next, r, done, _ = env_pend.step(np.array([0.0]))
    sleep(5.0)


print(w_range.tolist())
print(max_amps)


print("\nDone!")


#
