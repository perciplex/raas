import pigpio

from math import pi
import signal
import sys
# need to run daemon before you can run this
# `sudo pigpiod`

# https://github.com/gpiozero/gpiozero/issues/392
# https://github.com/pootle/pimotors
class Encoder():
    def __init__(self):
        self.steps_per_rev = 120*4
        pi = pigpio.pi()  
        self.A = False
        self.B = False
        self.step = 0
        def pressA(gpio, level, tick):
            self.A = True
            if self.B:
                self.step += 1
            else:
                self.step -= 1
        def releaseA(gpio, level, tick):
            self.A = False
            if self.B:
                self.step -= 1
            else:
                self.step += 1
        def pressB(gpio, level, tick):
            self.B = True
            if self.A:
                self.step -= 1
            else:
                self.step += 1
        def releaseB(gpio, level, tick):
            self.B = False
            if self.A:
                self.step += 1
            else:
                self.step -= 1
        pi.callback(14, pigpio.RISING_EDGE,pressA)
        pi.callback(14, pigpio.FALLING_EDGE,releaseA)
        pi.callback(15, pigpio.RISING_EDGE,pressB)
        pi.callback(15, pigpio.FALLING_EDGE,releaseB)
    def getDegree(self):
        return self.step / self.steps_per_rev * 360
    def getRadian(self):
        return self.step / self.steps_per_rev  * 2 * pi



class Motor():
    def __init__(self):
        self.forward_pin = 13
        self.backward_pin = 19
        # we need 2 pins? 1 for forward the other for reverse
        self.pi = pigpio.pi()  

        self.pi.set_mode(self.forward_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.backward_pin, pigpio.OUTPUT)
        self.pi.set_PWM_range(self.forward_pin, 1000)
        self.pi.set_PWM_range(self.backward_pin, 1000)
        self.pi.set_PWM_frequency(self.forward_pin, 10000)
        self.pi.set_PWM_frequency(self.backward_pin, 10000)
        def exit_gracefully(signum, frame):
            self.stop()
            sys.exit(0)
        signal.signal(signal.SIGINT, exit_gracefully)
        #signal.signal(signal.SIGTERM, exit_gracefully)
        
    def stop(self):
        self.set_torque(0)
    def set_torque(self, torque):
        # check if torque is in allowed range?
        if torque > 1000 or torque < -1000:
            print("FUCK_YOU_THAT_IS_NOT_A_TORQUE()")
            return 
        if torque >= 0:
            self.pi.set_PWM_dutycycle(self.forward_pin,  int(abs(torque)))
            self.pi.set_PWM_dutycycle(self.backward_pin, 0)
        elif torque < 0:
            self.pi.set_PWM_dutycycle(self.forward_pin,  0)
            self.pi.set_PWM_dutycycle(self.backward_pin, int(abs(torque)))
    def __del__(self): # this doesn't work. Appears to be killing pigpio first
        self.stop
    def __exit__(self):
        self.stop()





if __name__ == "__main__":
    from time import sleep
    encoder = Encoder()
    motor = Motor()

    while True:
        motor.set_torque(200)
        sleep(0.5)
        print("Step: ", encoder.step)
        motor.set_torque(-200)
        sleep(0.5)
        print("Step: ", encoder.step)
