#----------------------------------------
# Device Configuration for OLED Display
#
# [USAGE]
# - `import disp_device`
# - `device = disp_device.configure(context_name, width, height, display, interface, clockwise_rotation)`
#   - context_name (str) - The name of the caller.
#   - width (int) – The number of horizontal pixels.
#   - height (int) – The number of vertical pixels.
#   - display (str) - The name of the display driver, e.g., 'ssd1306'.
#   - interface (str) - One of 'i2c' or 'spi'.
#   - clockwise_rotation (int) – One of 0, 90, 180 or 270.
#----------------------------------------

import logging
import time

from demo_opts import get_device

#----------------------------------------
# Non-public Variables
#----------------------------------------

_context_name = None

#----------------------------------------
# Public Functions
#----------------------------------------

def configure(context_name, width, height, display, interface, clockwise_rotation = 0):
    global _context_name
    _context_name = context_name

    # Configure SPI
    if interface == 'spi':
        # Ensure GPIO is ready
        _ensure_gpio_ready()

    # Configure SSD1305
    if display == 'ssd1305':
        # Get device for SSD1306 and then configure it for SSD1305
        device = get_device(actual_args=['--display=ssd1306', f"--width={width}", f"--height={height}", f"--interface={interface}", f"--rotate={clockwise_rotation // 90}"])

        # (1) Set COM Output Scan Direction (0xC0)
        #   - remapped mode (0x08)
        device.command(0xC8)

        # (2) Set COM Pins Hardware Configuration (0xDA, 0x02)
        #   - Disable COM Left/Right remap (0x00)
        #   - Alternative COM pin configuration (0x10)
        device.command(0xDA, 0x12)

        if width == 128:
            # (3) Shift column start/end addresses
            device._colstart += 4 # 0 -> 4
            device._colend   += 4 # 128 -> 132

        return device

        # See also:
        #   - SSD1305 controller with 128x32 display issue
        #     <https://github.com/rm-hull/luma.oled/issues/309>
        #   - SSD1305 Data Sheet
        #     <https://cdn-shop.adafruit.com/datasheets/SSD1305.pdf>

    # Configure Other Devices
    else:
        # Get device
        return get_device(actual_args=[ f"--display={display}", f"--width={width}", f"--height={height}", f"--interface={interface}", f"--rotate={clockwise_rotation // 90}" ])

#----------------------------------------
# Non-public Functions
#----------------------------------------

def _ensure_gpio_ready():
    logger = logging.getLogger()
    gpiomem = '/dev/gpiomem'
    waiting = False
    while True:
        try:
            with open(gpiomem) as x:
                break
        except (FileNotFoundError, PermissionError):
            pass
        if not waiting:
            logger.info(f"{_context_name}: Waiting for '{gpiomem}' is ready")
            waiting = True
        time.sleep(1)
    if waiting:
	    logger.info(f"{_context_name}: Now '{gpiomem}' is ready")

#----------------------------------------
