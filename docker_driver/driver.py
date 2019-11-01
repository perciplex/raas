import pigpio

from math import pi
import atexit

# need to run daemon before you can run this
# `sudo pigpiod`

# https://github.com/gpiozero/gpiozero/issues/392
# https://github.com/pootle/pimotors
class Encoder:
    def __init__(self):
        self.steps_per_rev = 120 * 4
        pi = pigpio.pi()
        self.A = False
        self.B = False
        self.step = 0
        self.prevTick = pi.get_current_tick()
        self.vel = 0 # velocity is is ticks per microsecond

        def pressA(gpio, level, tick):
            self.A = True
            if self.B:
                self.step += 1
                self.vel = 1.0 / pigpio.tickDiff(self.prevTick, tick)
            else:
                self.step -= 1
                self.vel = -1.0 / pigpio.tickDiff(self.prevTick, tick)
            self.prevTick = tick

        def releaseA(gpio, level, tick):
            self.A = False
            if self.B:
                self.step -= 1
                self.vel = -1.0 / pigpio.tickDiff(self.prevTick, tick)
            else:
                self.step += 1
                self.vel = 1.0 / pigpio.tickDiff(self.prevTick, tick)
            self.prevTick = tick

        def pressB(gpio, level, tick):
            self.B = True
            if self.A:
                self.step -= 1
                self.vel = -1.0 / pigpio.tickDiff(self.prevTick, tick)
            else:
                self.step += 1
                self.vel = 1.0 / pigpio.tickDiff(self.prevTick, tick)
            self.prevTick = tick

        def releaseB(gpio, level, tick):
            self.B = False
            if self.A:
                self.step += 1
                self.vel = 1.0 / pigpio.tickDiff(self.prevTick, tick)
            else:
                self.step -= 1
                self.vel = -1.0 / pigpio.tickDiff(self.prevTick, tick)
            self.prevTick = tick

        pi.callback(15, pigpio.RISING_EDGE, pressA)
        pi.callback(15, pigpio.FALLING_EDGE, releaseA)
        pi.callback(14, pigpio.RISING_EDGE, pressB)
        pi.callback(14, pigpio.FALLING_EDGE, releaseB)

    def getDegree(self):
        return self.step / self.steps_per_rev * 360

    def getRadian(self):
        return self.step / self.steps_per_rev * 2 * pi
    def getRadPerSec(self): # convert microsceonds to seconds and ticks to rads.
        return self.vel * 1e6 * 2 * pi / self.steps_per_rev


class Motor:
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
        atexit.register(self.stop)

    def stop(self):
        self.set_command(0)


    def set_pendulum_torque(self, pend_torque):

        # This one is just a wrapper for set_command() that makes it so
        # you pass it a torque in the range [-2, 2].
        self.set_command(pend_torque*250.0)


    def set_command(self, command):
        # check if command is in allowed range?
        if command > 1000 or command < -1000:
            print("FUCK_YOU_THAT_IS_NOT_A_TORQUE()")
            return
        if command >= 0:
            self.pi.set_PWM_dutycycle(self.forward_pin, int(abs(command)))
            self.pi.set_PWM_dutycycle(self.backward_pin, 0)
        elif command < 0:
            self.pi.set_PWM_dutycycle(self.forward_pin, 0)
            self.pi.set_PWM_dutycycle(self.backward_pin, int(abs(command)))

    def set_torque(self, torque):
        self.set_command(torque / 0.01223)

    def __del__(self):  # this doesn't work. Appears to be killing pigpio first
        self.stop()

    def __exit__(self):
        self.stop()


if __name__ == "__main__":
    from time import sleep
    import zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    encoder = Encoder()
    motor = Motor()

    while True:
        #  Wait for next request from client
        try:
            (message_type, content) = socket.recv_pyobj()
            if message_type == "Command":
                motor.set_command(int(content))
            elif message_type == "Poll":
                socket.send_pyobj(( encoder.getRadian()  , encoder.getRadPerSec() ))
        except:
            pass
