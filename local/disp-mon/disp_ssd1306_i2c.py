#----------------------------------------
# Device Configuration for SSD1306 OLED Display connected via I2C
#
# [USAGE]
# - `from disp_ssd1306_i2c import configure_device`
# - `device = configure_device()`
#
# [CONFIGURATION]
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
#     - SDA: GPIO 2 (BSC1 SDA)
#     - SCL: GPIO 3 (BSC1 SCL)
#----------------------------------------

from demo_opts import get_device

def configure_device(width, height, contextName):
    # Get device for SSD1306 connected via I2C
    return get_device(actual_args=['--display=ssd1306', f"--width={width}", f"--height={height}", '--rotate=2', '--interface=i2c'])

#----------------------------------------
