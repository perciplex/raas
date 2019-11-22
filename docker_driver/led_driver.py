import re
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import multiprocessing

class LedMessage():
        def __init__(self, msg):
                self.msg = msg
                self.serial = spi(port=0, device=0, gpio=noop())
                self.device = max7219(self.serial, cascaded=4, block_orientation=90,rotate=2, blocks_arranged_in_reverse_order=True)
                self.device.contrast(2 * 16)
                self.thread = None

        def start(self):
                self.thread = multiprocessing.Process(target=self._write_led, args=(), kwargs={})
                self.thread.start()    

        def stop(self):
                if self.thread:
                        self.thread.terminate()
                self._clear_led() 

        def _write_led(self):  
                while True:
                        show_message(self.device, self.msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)

        def _clear_led(self):
                show_message(self.device, "", fill="white", font=proportional(LCD_FONT), scroll_delay=0)