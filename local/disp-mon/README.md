# Display Monitor (`disp-mon`)

## Setup

- `disp_mon.py` is a python program to periodically show device status on an OLED display.
- To setup `disp_mon.py` on the device, see:
  - [rpi_setup_oled_mon.sh](../../rpi_setup_oled_mon.sh)

### `Luma.OLED`

- Python module `Luma.OLED` is required. For the details, see:
  - [Luma.OLED](<luma.oled.md>)

### I2C

- If the display is connected via I2C, run the following commands to enable I2C.
  - `sudo raspi-config nonint do_i2c 0`
  - `sudo reboot`

### SPI

- If the display is connected via SPI, run the following commands to enable SPI.
  - `sudo raspi-config nonint do_spi 0`
  - `sudo reboot`

## Source Code

- Here are examples.
  - 128x32 OLED Display with SSD1306 display driver connected via I2C
    - [disp_mon.rpi-1.local.py](disp_mon.rpi-1.local.py)
  - 128x32 OLED Display with SSD1305 display driver connected via SPI
    - [disp_mon.rpi-4.local.py](disp_mon.rpi-4.local.py)
