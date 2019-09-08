import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
angles = pickle.load( open( "free_run.p", "rb" ) )

t = np.linspace(0,5,len(angles))

def decay_sin(t, omega, dtheta, offset, decay, amp):
    return amp * np.sin(omega * t + dtheta) * np.exp(- decay * t)  +  offset
opt, _ = curve_fit(decay_sin, t,angles)

print(opt)
plt.plot(t,angles)
plt.plot(t, decay_sin(t, *opt) )

# returns
# [ 5.28974506  0.56391819 -0.60565738  0.3810029   1.07262904]
# omega = 5.28 => f = 1.6806761990504149 Hz => 0.5950008032510844 s period
# 0.38 decay constant
plt.show()
'''
5.28 ought to be from gravity
omega^2 = 9.8 * 2 / l
l ~ 0.5m
===> 6.260990336999411
Similar. wasn't expecting to be on the dot for a mutiple reasons.


'''