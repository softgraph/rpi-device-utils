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

## Source Code Examples

### 128x32 OLED Display with SSD1306 display driver connected via I2C

- [disp_mon.service](disp_mon.service)
  - [disp_mon.rpi-1.local.py](disp_mon.rpi-1.local.py)
    - [disp_device.py](<disp_device.py>)
      - [demo_opts.py](<demo_opts.py>)
    - [disp_contents.py](<disp_contents.py>)

- Display Module
  - Clone of
    - 0.9 inch 128x32 OLED For Raspberry Pi
      - <https://www.adafruit.com/product/3527>

- Display Interface
  - Type: I2C
  - I2C Device Address: 0x3c (Read/Write=0x79/0x78)

| Signal | Pin               | Note |
|--------|-------------------|------|
| VCC    | 3.3V              |      |
| GND    | GND               |      |
| SDA    | GPIO 2 (BSC1 SDA) | I2C Data |
| SCL    | GPIO 3 (BSC1 SCL) | I2C Clock |

### 128x32 OLED Display with SSD1305 display driver connected via SPI

- [disp_mon.service](disp_mon.service)
  - [disp_mon.rpi-4.local.py](disp_mon.rpi-4.local.py)
    - [disp_device.py](<disp_device.py>)
      - [demo_opts.py](<demo_opts.py>)
    - [disp_contents.py](<disp_contents.py>)

- Display Module
  - 128×32, 2.23inch OLED display HAT for Raspberry Pi
    - <https://www.waveshare.com/2.23inch-oled-hat.htm>

- Display Interface
  - Type: SPI

| Signal | Pin                 | Note |
|--------|---------------------|------|
| VCC    | 3.3V                |      |
| GND    | GND                 |      |
| DIN    | GPIO 10 (SPI0 MOSI) | SPI Data Input |
| CLK    | GPIO 11 (SPI0 SCLK) | SPI Clock Input |
| CS     | GPIO 8  (SPI0 CE0)  | Chip Selection (***1**) |
| DC     | GPIO 24             | Data/Command Selection (***2**)     |
| RST    | GPIO 25             | Reset (***1**)     |

- ***1**: Low = Active
- ***2**: Low = Command, High = Data

### 128×64 OLED Display with SSD1309 display driver connected via SPI

- [disp_mon.service](disp_mon.service)
  - [disp_mon.rpi-2.local.py](disp_mon.rpi-1.local.py)
  - [disp_mon.rpi-3.local.py](disp_mon.rpi-1.local.py)
    - [disp_device.py](<disp_device.py>)
      - [demo_opts.py](<demo_opts.py>)
    - [disp_contents.py](<disp_contents.py>)

- Display Module
  - 1.51inch Transparent OLED, 128×64 Resolution, SPI/I2C Interfaces, light blue color display
    - <https://www.waveshare.com/1.51inch-transparent-oled.htm>

- Display Interface
  - Type: SPI

| Signal | Line   | Pin                 | Note |
|--------|--------|---------------------|------|
| VCC    | Red    | 3.3V                |      |
| GND    | Black  | GND                 |      |
| DIN    | Blue   | GPIO 10 (SPI0 MOSI) | SPI Data Input |
| CLK    | Yellow | GPIO 11 (SPI0 SCLK) | SPI Clock Input |
| CS     | Orange | GPIO 8 (SPI0 CE0)   | Chip Selection (***1**) |
| DC     | Green  | GPIO 24             | Data/Command Selection (***2**) |
| RST    | White  | GPIO 25             | Reset (***1**) |

- ***1**: Low = Active
- ***2**: Low = Command, High = Data

## GPIO Layout

| Line   | Pin         | #  | #  | Pin         | Line |
|--------|-------------|----|----|-------------|------|
|        | **3.3V**    | 1  | 2  | (5V)        |      |
|        | **GPIO 2**  | 3  | 4  | (5V)        |      |
|        | **GPIO 3**  | 5  | 6  | **GND**     |      |
|        | -           | 7  | 8  | -           |      |
|        | (GND)       | 9  | 10 | -           |      |
|        | -           | 11 | 12 | -           |      |
|        | -           | 13 | 14 | (GND)       |      |
|        | -           | 15 | 16 | -           |      |
| Red    | **3.3V**    | 17 | 18 | **GPIO 24** | Green |
| Blue   | **GPIO 10** | 19 | 20 | **GND**     | Black |
|        | -           | 21 | 22 | **GPIO 25** | White |
| Yellow | **GPIO 11** | 23 | 24 | **GPIO 8**  | Orange |
|        | (GND)       | 25 | 26 | -           |      |

- See also:
  - [Raspberry Pi / GPIO](<../../Raspberry Pi/gpio.md>)
