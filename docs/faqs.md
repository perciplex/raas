# FAQs

## What does my repo and script need?

The file that the system will run when your job is submitted must be called `run.py`. It can have other files/packages in it, but it must have that one to be run.

To build the env, it's nearly identical to using OpenAI gym:

```
import gym
import gym_raas

env = gym.make('RaasPendulum-v0')

# env.reset(), env.step(), etc...
```


## What packages can I use?

Since your repo will be run from within a Docker container that has no internet access, it can't pull arbitrary packages. However, it's built with many common packages you might use for ML/DL/RL:

* `numpy`
* `scipy`
* `gym==0.15.3`
* `torch==1.2.0`
* `tensorflow=2.3.0`


## How do I download my results?

There's a small download button under the plot, on the right hand side. This will download the episode data and stdout as a JSON file.


##
