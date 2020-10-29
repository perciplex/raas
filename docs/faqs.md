# FAQs

## What does my repo and script need?

The file that the system will run when your job is submitted must be called `run.py`. It can have other files/packages in it, but it must have that one to be run.

To build the env, it's nearly identical to using OpenAI gym:

```python
import gym
import gym_raas

env = gym.make('RaasPendulum-v0')

# env.reset(), env.step(), etc...
```


## What packages can I use?

Since your repo will be run from within a Docker container that has no internet access, it can't pull arbitrary packages. However, it's built with many common packages you might use for ML/DL/RL:

* `numpy`
* `scipy`
* `gym==0.17.3`
* `torch==1.5.0`
* `tensorflow=2.3.1`


## How do I download my results?

There's a small download button under the plot, on the right hand side. This will download the episode data and stdout as a JSON file.


## What are the physical parameters of the pendulum?

The gym-raas simulator is modified version of the stock OpenAI gym pendulum environment with parameters changed to match the measured dynamics of our physical pendulums. The simulation code with parameters may be found [here](https://github.com/perciplex/gym-raas/blob/41021e4ebf8efbd6ca8f96434313916c9252544f/gym_raas/envs/PendulumEnv.py#L90) and the methodology for measuring these parameters [here](https://www.philipzucker.com/system-identification-of-a-pendulum-with-scikit-learn/). The hardware gym environment is throttled to 20 steps per second to match the speed of the simulation.

However, the simulator is a significantly simplified model of the pendulum and is not 100% accurate to reality, as is always the case.
Godspeed and good luck!



