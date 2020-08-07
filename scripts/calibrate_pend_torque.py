import gym
import gym_raas
import numpy as np
import time
import pprint
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "--torque_start", type=float, default=0.0, help="The start torque to use"
)
parser.add_argument(
    "--torque_end", type=float, default=2.0, help="The end torque to use"
)
parser.add_argument(
    "--steps", type=int, default=10, help="The steps between the start and end torques"
)

# False unless you give the openai flag
parser.add_argument(
    "--openai", action="store_true", help="Use the openai pendulum env instead"
)
args = parser.parse_args()


obs = []
torque_range = np.linspace(args.torque_start, args.torque_end, args.steps)


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


if not HARDWARE:

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

        # env.render()
        print("Running with torque = {:.2f} now".format(t))
        thetas = []
        for _ in range(500):
            observation, reward, done, info = env.step([t])
            theta = np.arccos(observation[0])
            thetas.append(theta)
            # env.render()

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

d = {"name": name, "torques": torque_range.tolist(), "obs": obs}

print("\n")
pprint.pprint(d)


env.reset()
