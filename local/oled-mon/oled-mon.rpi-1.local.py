#! /usr/bin/env python

#----------------------------------------
# OLED Monitor
#
# [HARDWARE]
# - Display Module
#   - 128×32, 2.23inch OLED display HAT for Raspberry Pi
#     <https://www.waveshare.com/2.23inch-oled-hat.htm>
# - Display Driver
#   - SSD1305
#     <https://cdn-shop.adafruit.com/datasheets/SSD1305.pdf>
#     - Embedded 132 x 64 bit SRAM display buffer
# - Display Interface
#   - Type: SPI
#   - SPI Wiring
#     - VCC: 3.3V
#     - GND: GND
#     - DIN: SPI0 MOSI (BCM 10) # SPI data input
#     - CLK: SPI0 SCLK (BCM 12) # SPI clock input
#     - CS:  SPI0 CE0  (BCM 8)  # Chip selection, low active
#     - DC:  GPIO 24   (BCM 24) # Data/Command selection (high for data, low for command)
#     - RST: GPIO 25   (BCM 25) # Reset, low active
#----------------------------------------

import datetime
import time

from demo_opts import get_device
from luma.core.render import canvas # type: ignore

def device():
    # [SSD1306] get device
    device = get_device(actual_args=['--display=ssd1306', '--width=128', '--height=32', '--interface=spi'])
    # ['--spi-bus-speed=32000000']
    # [SSD1305] Set COM Output Scan Direction: remapped mode
    device.command(0xC8)
    # [SSD1305] Set COM Pins Hardware Configuration: Disable COM Left/Right remap + Alternative COM pin configuration
    device.command(0xDA, 0x12)
    # [SSD1305] Shift column start/end addresses
    device._colstart += 4 # 0 -> 4
    device._colend += 4   # 128 -> 132
    return device

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
