import RPi.GPIO as GPIO
from gpiozero import Button
from signal import pause

class Encoder():
    def __init__(self):
        self.A = Button(2)
        self.B = Button(2)
        self.step = 0
        def pressA():
            if self.B.is_pressed:
                self.step += 1
            else:
                self.step -= 1
        def releaseA():
            if self.B.is_pressed:
                self.step -= 1
            else:
                self.step += 1
        def pressB():
            if self.A.is_pressed:
                self.step -= 1
            else:
                self.step += 1
        def releaseB():
            if self.A.is_pressed:
                self.step += 1
            else:
                self.step -= 1
        self.A.when_pressed = pressA
        self.A.when_release = releaseA
        self.B.when_pressed = pressB
        self.B.when_released = releaseB
    

from time import sleep
encoder = Encoder()
while True:
    sleep(0.25)
    print("Step: ", encoder.step)