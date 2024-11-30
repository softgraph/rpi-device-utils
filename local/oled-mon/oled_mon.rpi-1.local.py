#! /usr/bin/env python

#----------------------------------------
# OLED Monitor
#
# [USAGE]
# - `python oled_mon.py &`
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
#
# [NOTE for SSD1305]
# - See:
#   - SSD1305 controller with 128x32 display issue
#     <https://github.com/rm-hull/luma.oled/issues/309>
#----------------------------------------

from collections import deque
import datetime
import logging
import os.path
import time

from demo_opts import get_device
from luma.core.render import canvas # type: ignore

logger = logging.getLogger()
name = os.path.basename(__file__)

deque_temp = deque([],maxlen=128)

def main():
    try:
        ensure_gpio_ready()
        device = configure_device()
        monitor(device)
    except KeyboardInterrupt:
        pass

def ensure_gpio_ready():
    gpiomem = '/dev/gpiomem'
    logger.info(f"{name}: Waiting for '{gpiomem}' is ready")
    while True:
        try:
            with open(gpiomem) as x:
                break
        except (FileNotFoundError, PermissionError):
            pass
        time.sleep(1)
    logger.info(f"{name}: Now '{gpiomem}' is ready")

def configure_device():
    # [SSD1306] get device
    device = get_device(actual_args=['--display=ssd1306', '--width=128', '--height=32', '--interface=spi'])
    # [SSD1305] Set COM Output Scan Direction: remapped mode
    device.command(0xC8)
    # [SSD1305] Set COM Pins Hardware Configuration: Disable COM Left/Right remap + Alternative COM pin configuration
    device.command(0xDA, 0x12)
    # [SSD1305] Shift column start/end addresses
    device._colstart += 4 # 0 -> 4
    device._colend += 4   # 128 -> 132
    return device

def monitor(device):
    count_plane_0 = 3
    count_plane_1 = count_plane_0 * 2
    i = 0
    while True:
        update()
        with canvas(device) as dc:
            draw_common(dc)
            if i < count_plane_0:
                draw_plane_0(dc)
            elif i < count_plane_1:
                draw_plane_1(dc)
        i += 1
        if i >= count_plane_1:
            i = 0
        time.sleep(1)

def update():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as fc:
            temp = int(fc.read())
            deque_temp.append(temp)
    except (FileNotFoundError, PermissionError):
        pass

def draw_common(dc):
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    temp = deque_temp[-1]
    str_temp = "{:.2f} °C".format(temp / 1000)
    # dc.rectangle(device.bounding_box, outline="white")
    dc.text((85, -1), str_time, fill="white")
    dc.text(( 0, -1), str_temp, fill="white")

def draw_plane_0(dc):
    x = 0
    for temp in deque_temp:
        y = - int(temp / 1000) + 66
        if y < 0: y = 0
        elif y > 31: y = 31
        dc.point((x,y), fill="white")
        x += 1

def draw_plane_1(dc):
    str_midi = ''
    try:
        with open('/var/tmp/local/midi-con.txt') as fc:
            str_midi = fc.readline().rstrip()
    except (FileNotFoundError, PermissionError):
        pass
    if len(str_midi) > 0:
        dc.text((0, 21), str_midi, fill="white")
    else:
        draw_plane_0(dc)

if __name__ == "__main__":
    main()
