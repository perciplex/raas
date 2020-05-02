from sys import path

path.append(r"/home/pi/raas/scripts/casadi")
from casadi import *


import matplotlib.pyplot as plt


T = 3
dt = 0.05
N = int(T / dt)
T = N * dt

# pendulum constants
omega = 5.28
omega2 = omega ** 2
max_torque = (
    2 * 0.01223 * 500
)  # factor of 2 cause I think I messed up the force calculation
opti = casadi.Opti()

x = opti.variable(N)
v = opti.variable(N)
u = opti.variable(N - 1)


x_init = opti.parameter()
v_init = opti.parameter()
opti.set_value(x_init, 0.0001)
opti.set_value(v_init, 0.0)
# https://epubs.siam.org/doi/pdf/10.1137/16M1062569
constraints = [x[0] == x_init, v[0] == v_init]
for i in range(N - 1):
    constraints += [x[i + 1] == (x[i] + dt * v[i])]
    constraints += [v[i + 1] == (v[i] - dt * omega2 * sin(x[i + 1]) + u[i] * dt)]
    constraints += [u[i] <= max_torque, u[i] >= -max_torque]

cost = sum([(cos(x[i]) + 1) ** 2 for i in range(N)]) + 0.01 * sum(
    [u[i] * u[i] for i in range(N - 1)]
)

opti.subject_to(constraints)
opti.minimize(cost)
p_opts = {"expand": True}
s_opts = {"max_iter": 1000}
opti.solver("ipopt", p_opts, s_opts)
sol = opti.solve()
"""
from driver import Encoder, Motor
import time

motor = Motor()
encoder = Encoder()

angle = encoder.get_angle()
old_angle = angle
t = time.time()
old_t = t+0.1

for i in range(100):
    #measure
    angle = encoder.getRadian()
    t = time.time()
    dt = t - old_t
    v_angle = (angle-old_angle) / dt

    #set new initial conditions
    opti.set_value(x_init, angle)
    opti.set_value(v_init, v_angle)
    
    #warm start 
    opti.set_initial(sol.value_variables())
    lam_g0 = sol.value(opti.lam_g)
    opti.set_initial(opti.lam_g, lam_g0)
    sol = opti.solve()

    motor.set_torque(ol.value(u)[0])
    old_angle = angle
    old_t = t

"""

x = sol.value(x)
v = sol.value(v)
u = sol.value(u)
print(x)

plt.plot(x, label="theta")
plt.plot(u, label="torque")
plt.plot(v, label="theta")
plt.legend()
plt.show()
