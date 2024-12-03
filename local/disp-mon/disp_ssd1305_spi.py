#----------------------------------------
# Device Configuration for SSD1305 OLED Display connected via SPI
#
# [USAGE]
# - `from disp_ssd1305_spi import configure_device`
# - `device = configure_device()`
#
# [CONFIGURATION]
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
#     - DI:  GPIO 10 (SPI0 MOSI) # SPI data input
#     - CLK: GPIO 12 (SPI0 SCLK) # SPI clock input
#     - CS:  GPIO 8  (SPI0 CE0) # Chip selection, low active
#     - DC:  GPIO 24 # Data/Command selection (high for data, low for command)
#     - RST: GPIO 25 # Reset, low active
# - See:
#   - SSD1305 controller with 128x32 display issue
#     <https://github.com/rm-hull/luma.oled/issues/309>
#----------------------------------------

from demo_opts import get_device
from disp_gpio import ensure_gpio_ready

def configure_device(contextName):
    # Ensure GPIO is ready
    ensure_gpio_ready(contextName)

    # Get device for SSD1306 connected via SPI
    device = get_device(actual_args=['--display=ssd1306', '--width=128', '--height=32', '--interface=spi'])

    # Configure for SSD1305

    # - Set COM Output Scan Direction (0xC0)
	#   - remapped mode (0x08)
    device.command(0xC8)

    # - Set COM Pins Hardware Configuration (0xDA, 0x02)
	#   - Disable COM Left/Right remap (0x00)
	#   - Alternative COM pin configuration (0x10)
    device.command(0xDA, 0x12)

    # - Shift column start/end addresses
    device._colstart += 4 # 0 -> 4
    device._colend += 4   # 128 -> 132

    return device

#----------------------------------------
