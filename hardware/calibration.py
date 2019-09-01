'''
It would be nice to pre calibrate the motor to give the user full torque control

Methodology:
- Give motor inputs. Random? Sinusoial? Ramp?
- fit motor/dynamic model (differential model? Finite difference for derivatives?)

\ddot{\theta} = \sum_m  a_n sin(n theta) + b_n thetadot + command
I dunno.
Or just a polynomial fit of a couple subsequent time points and the command.
?

'''
from driver import Encoder, Motor
from time import sleep
motor = Motor()
encoder = Encoder()
angles = []
torques = []
for t in range(10000):
    torque = random * 1000
    torques.append(torque)
    motor.set_torque( torque )
    angles.append(encoder.getRadians())
    # maybe a consistent fps?
    sleep(0.01)

# building up features
np.array(torques)
angles = np.array(angles)
s1 = np.sin(angles)
c1 = np.cos(angles)
s2 = np.sin(2 * angles)
sc = s1 * c1
c2 = np.cos(2 * angles)
ss = s1[1:] * s1[:-1]
sc = s1[1:] * c1[:-1]
cc = c1[1:] * c1[:-1]

np.stack( [s1,c1, s2, ss, sc, cc] )
