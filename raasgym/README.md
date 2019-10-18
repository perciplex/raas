# RaaS Gym

To install
```python
python3 setup.py sdist bdist_wheel
```

install pigpiod if intended to run on real hardware
Set RAASPI variable in python enviroment

Notes:
Build library


OPtions:
We could keep a hardware flag in the init here
read an environemtn variables?
Sepeerate SymPendulum and PhysPendulum files
Completely seperate packages.
Where do we keep the driver code? Also needing pigpiod


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





