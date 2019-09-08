from driver import Encoder, Motor
from time import sleep

e = Encoder()
m = Motor()

time = 1.0
dt = 0.01
steps = time / dt

angles = []

m.set_torque(500)
for i in range(steps):
    sleep(dt)
    angles.append(e.getRadian())
m.stop()

import matplotlib.pyplot as plt

plt.plot(angles)

plt.show()