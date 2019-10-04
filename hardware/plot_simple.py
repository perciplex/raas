import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

angles = pickle.load(open("simple_run.p", "rb"))

t = np.linspace(0, 1, len(angles))
"""
def decay_sin(t, omega, dtheta, offset, decay, amp):
    return amp * np.sin(omega * t + dtheta) * np.exp(- decay * t)  +  offset
opt, _ = curve_fit(decay_sin, t,angles)

print(opt)
"""
plt.plot(t, angles)
plt.title("command of 500")
plt.xlabel("time (s)")
plt.ylabel("radians")
# plt.plot(t, decay_sin(t, *opt) )


plt.show()
