import numpy as np
from raasgym.driver import Encoder, Motor

motor = Motor()
encoder = Encoder()

while True:
    angle = encoder.getRadian()
    torque = 1000 * np.sin(angle)
    motor.set_torque(torque)
