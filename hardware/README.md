# Pendulum Hardware

The pendulum is built using easily available hardware. The following are instructions for purchase and assembly.

## Bill of Materials

- Raspberry Pi (We use a model 4)
  + Power Supply for Pi
  + SD card for Pi
- L298N Motor Driver Board.
- Ribbon cable
- Motor with built in encoder?
- Power Supply?
- Paint Stirrer Rod. Only the best for us!
- Mount
- Aluminum Axle Mount plate 


Amazon shopping cart link : https://www.amazon.com/ideas/amzn1.account.AHWUEKBOXRZZ2YOBITVMXOZ7P2XA/2R26EST3LRFIO

## Pi Setup
Use Raspbian lite edition
Follow instructions

For an easier time, use neqbs or pibakery

Using a monitor and keyboard will make it easier

Plugging into ethernet as compared to wifi will be easier.

## Pendulum Construction


## Hooking the Pi up to the Pendulum

The Pi needs to be connected to 2 channels of the motor driver for forward and backward.
The encoder requires 4 wires.



https://www.raspberrypi.org/documentation/usage/gpio/README.md

https://www.raspberrypi.org/documentation/usage/gpio/images/gpio-numbers-pi2.png

"Hardware PWM available on GPIO12, GPIO13, GPIO18, GPIO19"
So we should probably use one of those.


## Calibration

Calibration programs and procedure.

The motor has interesting control charactersitics. By fitting measured data to a motor model, we can account for these dynamics. 

It is also possible to just get a machine learned approach to work on an uncalibrated system.






