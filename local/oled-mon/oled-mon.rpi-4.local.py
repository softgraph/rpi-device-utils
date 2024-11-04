#! /usr/bin/env python

#----------------------------------------
# OLED Monitor
#
# [HARDWARE]
# - Display Module
#   - 0.9 inch 128x32 OLED For Raspberry Pi
#     <https://www.adafruit.com/product/3527>
# - Display Driver
#   - SSD1306
#     <https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf>
#     - Embedded 128 x 64 bit SRAM display buffer
# - Display Interface
#   - Type: I2C
#   - I2C Device Address: 0x3c (Read/Write=0x79/0x78)
#   - I2C Wiring
#     - VCC: 3.3V
#     - GND: GND
#     - SDA: BSC1 SDA (BCM 2)
#     - SCL: BSC1 SCL (BCM 3)
#----------------------------------------

import datetime
import time

from demo_opts import get_device
from luma.core.render import canvas # type: ignore

def device():
    # [SSD1306] get device
    return get_device(actual_args=['--display=ssd1306', '--width=128', '--height=32', '--rotate=2', '--interface=i2c'])

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

if __name__ == "__main__":
    try:
        device = device()
        main()
    except KeyboardInterrupt:
        pass
