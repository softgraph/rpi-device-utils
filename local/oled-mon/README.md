# `oled-mon`

## Setup

- `oled-mon.py` is a python program to periodically show device status on an OLED display.
- To setup `oled-mon.py` on the device, see:
  - [rpi_setup_oled-mon.sh](../../rpi_setup_oled-mon.sh)
- Python module `Luma.OLED` is required. For the detail, see:
  - [Luma.OLED](<luma.oled.md>)

## Source Code

- Here are examples.
  - SSD1305 display driver connected via SPI
    - [oled-mon.rpi-1.local.py](oled-mon.rpi-1.local.py)
  - SSD1306 display driver connected via I2C
    - [oled-mon.rpi-4.local.py](oled-mon.rpi-4.local.py)
