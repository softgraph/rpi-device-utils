#! /usr/bin/env python

#----------------------------------------
# OLED Monitor
#
# [USAGE]
# - `python oled_mon.py &`
#
# [HARDWARE]
# - Display Module
#   - Clone of
#     - 0.9 inch 128x32 OLED For Raspberry Pi
#       <https://www.adafruit.com/product/3527>
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

from collections import deque
import datetime
import time

from demo_opts import get_device
from luma.core.render import canvas # type: ignore

def device():
    # [SSD1306] get device
    return get_device(actual_args=['--display=ssd1306', '--width=128', '--height=32', '--rotate=2', '--interface=i2c'])

def monitor():
    deque_temp = deque([],maxlen=128)
    while True:
        now = datetime.datetime.now()
        str_time = now.strftime("%H:%M:%S")
        str_temp = ''
        try:
            with open('/sys/class/thermal/thermal_zone0/temp') as fc:
                temp = int(fc.read())
                deque_temp.append(temp)
                str_temp = "{:.2f} °C".format(temp / 1000)
        except (FileNotFoundError, PermissionError):
            str_temp = '-'
        with canvas(device) as dc:
            dc.text((84, 0), str_time, fill="white")
            dc.text(( 0, 0), str_temp, fill="white")
            x = 0
            for temp in deque_temp:
                y = - int(temp / 1000) + 66
                if y < 0: y = 0
                elif y > 31: y = 31
                dc.point((x,y), fill="white")
                x += 1
        time.sleep(1)

if __name__ == "__main__":
    try:
        device = device()
        monitor()
    except KeyboardInterrupt:
        pass
