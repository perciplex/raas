from driver import Encoder, Motor
from time import sleep, time
import pickle

e = Encoder()
m = Motor()

T = 1.0
dt = 0.01
steps = int(T / dt)


anglemap = {}

<<<<<<< HEAD:hardware/simple_run.py
for torque in range(200, 1001, 200):
=======
for command in range(200,1001,200):
>>>>>>> ee553e917cadfc8d2b1fb8a09e71a3726ad2380e:hardware/calibration_scripts/simple_run.py
    angles = []
    start_time = time()
    m.set_command(command)
    for i in range(steps):
        sleep(dt)
        angles.append(e.getRadian())
    m.stop()
    total_time = time() - start_time
    print(total_time)
    anglemap[command] = angles
    sleep(2)


pickle.dump(anglemap, open("simple_run.p", "wb"))
