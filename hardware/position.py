from raasgym.driver import Encoder, Motor
import numpy as np

motor = Motor()
encoder = Encoder()

while True:
    angle = encoder.getRadian()
    torque = 1000 * np.sin(angle)
    motor.set_torque(torque)
