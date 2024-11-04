#! /usr/bin/env python

#----------------------------------------
# Hardware
# - Display
#   - 2.23 inch OLED
#   - 128×32, monochrome
#   - <https://www.waveshare.com/2.23inch-oled-hat.htm>
# - Display Driver
#   - SSD1305
#     - <https://cdn-shop.adafruit.com/datasheets/SSD1305.pdf>
# - Display Interface
#   - SPI
#----------------------------------------

import datetime
import math
import time

from demo_opts import get_device
from luma.core.render import canvas # type: ignore

def main():
    latest_date = ""
    while True:
        now = datetime.datetime.now()
        date = now.strftime("%Y.%m.%d %H:%M:%S")
        if latest_date != date:
            latest_date = date
            with canvas(device) as draw:
                draw.text((0, 0), date, fill="white")
        time.sleep(1)

def prepare_for_ssd1305_w132(device): # `device` should be a class `ssd1306` of width 128
    # Set COM Output Scan Direction: remapped mode
    device.command(0xC8)
    # Set COM Pins Hardware Configuration: Disable COM Left/Right remap + Alternative COM pin configuration
    device.command(0xDA, 0x12)
    # Update column start/end addresses
    device._colstart += 4 # 0 -> 4
    device._colend += 4   # 128 -> 132

if __name__ == "__main__":
    try:
        device = get_device()
        prepare_for_ssd1305_w132(device)
        main()
    except KeyboardInterrupt:
        #device.cleanup()
        pass
