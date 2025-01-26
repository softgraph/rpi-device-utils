# Display and Monitor (`disp-mon`)

## Setup

- `disp_mon.py` is a python program to periodically show device status on an OLED display.
- To setup `disp_mon.py` on the device, see:
  - [rpi_setup_oled_mon.sh](../../rpi_setup_oled_mon.sh)

### `luma.oled`

- Python module `luma.oled` is required.
- For the details, see:
  - [`luma.oled`](<luma.oled.md>)

### `RPi.GPIO`

- Python module `RPi.GPIO` is required for the following cases.
  - The OLED display is connected via SPI
  - Buttons are connected via GPIO
- For the details, see:
  - [`RPi.GPIO`](<RPi.GPIO.md>)

### I2C

- If the display is connected via I2C, run the following commands to enable I2C.
  - `sudo raspi-config nonint do_i2c 0`
  - `sudo reboot`

### SPI

- If the display is connected via SPI, run the following commands to enable SPI.
  - `sudo raspi-config nonint do_spi 0`
  - `sudo reboot`

## Source Code Examples

### 128 x 32 or 64 OLED Display with SSD1306 display driver connected via I2C

- [disp_mon.service](disp_mon.service)
  - [disp_mon.rpi-1.local.py](disp_mon.rpi-1.local.py) (128 x 64)
  - [disp_mon.rpi-2.local.py](disp_mon.rpi-2.local.py) (128 x 32)
    - [disp_device.py](<disp_device.py>)
      - [demo_opts.py](<demo_opts.py>)
    - [disp_contents.py](<disp_contents.py>)

- Display Module
  - 0.9 inch 128 x 32 OLED Display For Raspberry Pi
    - Clone of
      - <https://www.adafruit.com/product/3527>
  - 0.96 inch 128 x 64 OLED Display For Raspberry Pi
    - Similar to the above, but 128 x 64.

- Display Interface
  - Type: I2C
  - I2C Device Address: 0x3c (Read/Write=0x79/0x78)

| Signal | Pin               | Note |
|--------|-------------------|------|
| VCC    | 3.3V              |      |
| GND    | GND               |      |
| SDA    | GPIO 2 (BSC1 SDA) | I2C Data |
| SCL    | GPIO 3 (BSC1 SCL) | I2C Clock |

### 128 x 32 OLED Display with SSD1305 display driver connected via SPI

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
| DC     | GPIO 24             | Data/Command Selection (***2**) |
| RST    | GPIO 25             | Reset (***1**) |

- ***1**: Low = Active
- ***2**: Low = Command, High = Data

### 128 × 64 OLED Display with SSD1309 display driver connected via SPI

- [disp_mon.service](disp_mon.service)
  - [disp_mon.rpi-3.local.py](disp_mon.rpi-3.local.py)
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
| ***1** | **3.3V**    | 1  | 2  | (5V)        | ***1** |
| ***1** | **GPIO 2**  | 3  | 4  | (5V)        | ***1** |
| ***1** | **GPIO 3**  | 5  | 6  | **GND**     | ***1** |
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
|        | -           | 27 | 28 | -           |      |
|        | -           | 29 | 30 | (GND)       |      |
|        | -           | 31 | 32 | -           |      |
| ***2** | **GPIO 13** | 33 | 34 | (GND)       |      |
| ***2** | **GPIO 19** | 35 | 36 | -           |      |
| ***2** | **GPIO 26** | 37 | 38 | -           |      |
| ***2** | (GND)       | 39 | 40 | -           |      |

- Note
  - ***1**:
    - GPIO 2 x 3 pin for I2C
  - ***2**:
    - GPIO 1 x 4 pin for 3-Button Array

- See also:
  - [Raspberry Pi / GPIO](<../../Raspberry Pi/gpio.md>)

## Technical Notes

### User Service (`systemd`)

- The following user service is used for `disp-mon`.
  - [disp_mon.service](disp_mon.service)

- Run the command below to show the logging for the service.

```shell
$ journalctl --no-pager -b --user -u disp_mon
:
```
