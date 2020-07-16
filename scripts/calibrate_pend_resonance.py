import gym
import gym_raas
import numpy as np
import time

print("Setting up env...")
env = gym.make("raaspendulum-v0")
# env = gym.make("Pendulum-v0")
print("Set up!")
env.reset()

obs = []
# w_range = np.linspace(3, 4, 2)
w_range = np.linspace(1, 7, 40)
SIMULATION = True
time_incr = 0.05
max_torque = 0.3
max_amps = []
if SIMULATION:
    for w in w_range:
        print("\nResetting env...")
        found_init = False
        # print(f'Original env.state is {env.state}')
        while not found_init:
            env.reset()
            th, thdot = env.state
            if abs(th) > 3.1 and abs(thdot) < 0.05:
                print("found good init!")
                print(env.state)
                found_init = True

        # env.render()
        print("Running with freq = {:.2f} now".format(w))
        max_ep_amp = None
        thetas = []
        for t in range(400):
            if np.sin(w * t * time_incr) > 0:
                mult = 1.0
            else:
                mult = -1.0
            # action = np.array([2.0 * np.sin(w * t * time_incr)])
            observation, reward, done, info = env.step([mult * max_torque])
            x, y, _ = observation
            theta = abs(np.arccos(x))

            if (max_ep_amp is None) or (theta < max_ep_amp):
                max_ep_amp = theta
            # env.render()
            # time.sleep(0.2)

        print("\nMax angle found: ", max_ep_amp)
        max_amps.append(max_ep_amp)
        obs.append([np.cos(np.mean(thetas))])


else:

    try:
        for t in torque_range:
            print("Running with torque = {:.2f} now".format(t))
            for _ in range(10):
                observation, reward, done, info = env.step([t])
                time.sleep(0.5)
            obs.append(observation)

    except:
        print("Stopped!")


print("\nRes freqs:")
print(w_range.tolist())

print("\nMax amplitudes:")
print(max_amps)


env.reset()
