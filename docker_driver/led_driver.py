import re
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import multiprocessing

# a class for displaying a single message on the LED matrix display

class LedMessage():
        def __init__(self, msg):
                self.msg = msg # store the message content
                self.serial = spi(port=0, device=0, gpio=noop()) # open a serial port
                self.device = max7219(self.serial, cascaded=4, block_orientation=90,rotate=2, blocks_arranged_in_reverse_order=True) # initialize a matrix display object
                self.device.contrast(6) # decrease the contrast so that it looks okay on video
                self.process = None # initialize a variable that will store the process 

        def __del__(self):
                self.stop() # stop any message and clear
                self.serial.cleanup() # clean up the serial port


        def start(self):
                self.process = multiprocessing.Process(target=self._show_msg, args=(), kwargs={}) # initialize a process to repeatedly write the message
                self.process.start() # start the process

        def stop(self):
                if self.process: # check if a process is actually running
                        self.process.terminate() # if it has, stop it
                        self.process = None # reset the process to none
                self._clear() # clear the display

        def _show_msg(self):  
                while True: # forever
                        show_message(self.device, self.msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05) # display the scrolling message

        def _clear(self):
                show_message(self.device, "", fill="white", font=proportional(LCD_FONT), scroll_delay=0) # write a blank message to clear the screen