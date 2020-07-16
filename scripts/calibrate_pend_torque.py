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
torque_range = np.linspace(0, 2.0, 10)
SIMULATION = True

if SIMULATION:

    for t in torque_range:
        print("Resetting env...")
        found_init = False
        # print(f'Original env.state is {env.state}')
        while not found_init:
            env.reset()
            th, thdot = env.state
            if abs(th) > 3.1 and abs(thdot) < 0.1:
                print("found good init!")
                print(env.state)
                found_init = True

        env.render()
        print("Running with torque = {:.2f} now".format(t))
        thetas = []
        for _ in range(500):
            observation, reward, done, info = env.step([t])
            theta = np.arccos(observation[0])
            thetas.append(theta)
            env.render()

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


print("\nTorques:")
print(torque_range.tolist())

print("\nObservations:")
[print(o) for o in obs]
print()
print(obs)

env.reset()
