# RaaS Gym

This is a python library designed to mimic the interface of the OpenAI Pendulum-v0 environment.

A short use example

```python
#TODO
import ?


while not done:
    yada yaday = env.action(?)

gym.save(my_data, format="json")

```

Upon the gym returning `done = True`, you have 1 second remaining before your program is forcefully stopped. Make sure to save your data before that time.

We request that you courteously call gym.close() to end your sesssion early if you do not need all of your allocated time.

# Data Return
You may save data to be returned to you in mutiple ways.
You have a total data budget of x MB.

- All prints to the standard out
- All data saved to the logs folder will be returned
- You may also call gym.save(, format=format), where format may be one of "pickle", "json", "csv" 





