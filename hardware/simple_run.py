from driver import Encoder, Motor
from time import sleep, time
import pickle 

e = Encoder()
m = Motor()

T = 1.0
dt = 0.01
steps = int(T / dt)


anglemap = {}

for torque in range(200,1001,200):
    angles = []
    start_time = time()
    m.set_torque(torque)
    for i in range(steps):
        sleep(dt)
        angles.append(e.getRadian())
    m.stop()
    total_time = time() - start_time
    print(total_time)
    anglemap[torque] = angles
    sleep(1.5)
    

pickle.dump(anglemap, open( "simple_run.p", "wb"))







