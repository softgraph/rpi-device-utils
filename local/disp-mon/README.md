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
    - [disp_ssd1306_i2c.py](<disp_ssd1306_i2c.py>)
      - VCC: 3.3V
      - GND: GND
      - SDA: GPIO 2 (BSC1 SDA)
      - SCL: GPIO 3 (BSC1 SCL)
  - 128x32 OLED Display with SSD1305 display driver connected via SPI
    - [disp_mon.rpi-4.local.py](disp_mon.rpi-4.local.py)
    - [disp_ssd1305_spi.py](<disp_ssd1305_spi.py>)
      - VCC: 3.3V
      - GND: GND
      - DI:  GPIO 10 (SPI0 MOSI)
      - CLK: GPIO 11 (SPI0 SCLK)
      - CS:  GPIO 8  (SPI0 CE0)
      - DC:  GPIO 24
      - RST: GPIO 25

## GPIO Pins

| #  |             |  |
|----|-------------|--|
| 1  | **3.3V**    | (5V) |
| 3  | **GPIO 2**  | (5V) |
| 5  | **GPIO 3**  | **GND** |
| 7  | -           | - |
| 9  | -           | - |
| 11 | -           | - |
| 13 | -           | - |
| 15 | -           | - |
| 17 | **3.3V**    | **GPIO 24** |
| 19 | **GPIO 10** | **GND** |
| 21 | -           | **GPIO 25** |
| 23 | **GPIO 11** | **GPIO 8** |

- See also:
  - [Raspberry Pi / GPIO](<../../Raspberry Pi/gpio.md>)
