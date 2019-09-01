 
#import RPi.GPIO as GPIO
import pigpio


# https://github.com/gpiozero/gpiozero/issues/392
# https://github.com/pootle/pimotors
class Encoder():
    def __init__(self):
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

    

from time import sleep
encoder = Encoder()
while True:
    sleep(0.25)
    print("Step: ", encoder.step)