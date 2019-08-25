# Sketch of pi driver
import zmq
import time


# import RPi.GPIO as GPIO
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
class Motor():
    def __init__(self);
        forward_pin = 8
        backward_pin = 9
        # we need 2 pins? 1 for forward the other for reverse
        GPIO.setup(motor_pin, GPIO.OUT)
        forward_pwm = GPIO.PWM(motor_pin, frequency)
        forward_pwm.start(0) 
    def set_torque(self, torque):
        # check if torque is in allowed range?
        if torque > 100 or torque < -100:
            return FUCK_YOU_THAT_IS_NOT_A_TORQUE()
        if torque == 0:
        elif torque > 0:
            forward_pwm.ChangeDutyCycle(torque)
        elif torque < 0:
    def __del__(self):
        p.stop()
        GPIO.cleanup()


class Encoder:
    def __init__(self):
        pass

motor = Motor()
encoder = Encoder()

context = zmq.Context()
socket = context.socket(zmq.REP)
port = 5555
socket.bind("tcp://*:%s" % port)

while True:
    #regular loop
    message = socket.recv()
    # This message actually does need be scrubbed.
    # in pricniple it is coming from user controlled code.
    print "Received request: ", message
    motor.set_torqu(message.torque)
    pendulum_state = encoder.get_state():
    socket.send(pendulum_state)