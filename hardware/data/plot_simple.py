import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

anglemap = pickle.load(open("simple_run.p", "rb"))

t = np.linspace(0, 1, len(anglemap[200]))
"""
def decay_sin(t, omega, dtheta, offset, decay, amp):
    return amp * np.sin(omega * t + dtheta) * np.exp(- decay * t)  +  offset
opt, _ = curve_fit(decay_sin, t,angles)

print(opt)
"""


def d2(x):
    x = np.array(x)
    return 2 * x[1:-1] - x[:-2] - x[2:]


stop = []
keys = []
ps = []
for key, angles in anglemap.items():
    keys.append(key)
    angles = np.array(angles)
    angles = angles - angles[0]
    plt.plot(t, angles, label=key)
    # print(np.average(d2(angles[:30]))/0.01/0.01)
    # print(np.polyfit(t[:30], angles[:30],2))
    p = np.polyfit(t, angles, 2)
    ps.append(p)
    plt.plot(t, np.polyval(p, t))
    print(p)
    # stop.append(angles[-1])
    pv = np.polyder(p, 1)
    pa = np.polyder(p, 2)


# plt.plot([200,400,600,800,1000], [0.6,2.2,4,6.1,7.82])
# plt.plot([200,400,600,800,1000], stop)
plt.title("Acceleration from Stop")
plt.xlabel("time")
plt.ylabel("Radians")
plt.legend()
# plt.plot(t, decay_sin(t, *opt) )
plt.figure()
ps = np.array(ps)
keys = np.array(keys)
print(keys.shape)
print(ps[:, 0])
plt.plot(keys, ps[:, 0])
fred = np.polyfit(keys, ps[:, 0], 1)
print("what", fred)
print(fred.shape)
plt.plot(keys, np.polyval(fred, keys))


# accel = 0.01223007 * command +  -1.77304897 # Woah. The offset is that good?
# accel = 0.01223 * command
plt.show()

# omega *


"""
[0.57428365 0.21209431 0.00341285]
[ 3.06168476  0.77146264 -0.05611183]
[ 5.77202229  1.0760587  -0.0721008 ]
[ 8.16354387  1.61105509 -0.10276442]
[10.25342087  2.01530717 -0.12853008]
"""
