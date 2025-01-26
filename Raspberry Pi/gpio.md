# Raspberry Pi / GPIO

## Pin Numbers

- raspberrypi.com
  - Raspberry Pi Documentation
    - [Raspberry Pi hardware](<https://www.raspberrypi.com/documentation/computers/raspberry-pi.html>)
      - [GPIO and the 40-pin header](<https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio>)
        - ![GPIO-Pinout-Diagram-2.png](<https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png>)
        - ![GPIO.png](<https://www.raspberrypi.com/documentation/computers/images/GPIO.png>)

## Pin Functions

- [`$ pinctrl -c bcm2835`](<gpio/bcm2835.csv>)
- [`$ pinctrl -c bcm2711`](<gpio/bcm2711.csv>)
- [`$ pinctrl -c bcm2712`](<gpio/bcm2712.csv>)

## Pins for I2C Slave

### BCM2835 (Raspberry Pi except for the models below)

|        |          |      |         |                |            |  |
|--------|----------|------|---------|----------------|------------|--|
| GPIO18 | PCM_CLK  | SD10 | DPI_D14 | I2CSL_SDA_MOSI | SPI1_CE0_N | PWM0 |
| GPIO19 | PCM_FS   | SD11 | DPI_D15 | I2CSL_SCL_SCLK | SPI1_MISO  | PWM1 |
| GPIO20 | PCM_DIN  | SD12 | DPI_D16 | I2CSL_MISO     | SPI1_MOSI  | GPCLK0 |
| GPIO21 | PCM_DOUT | SD13 | DPI_D17 | I2CSL_CE_N     | SPI1_SCLK  | GPCLK1 |

### BCM2711 (Raspberry Pi 4, 400, CM 4)

|        |            |     |        |                |      |  |
|--------|------------|-----|--------|----------------|------|--|
| GPIO8  | SPI0_CE0_N | SD0 | DPI_D4 | I2CSL_CE_N     | TXD4 | SDA4 |
| GPIO9  | SPI0_MISO  | SD1 | DPI_D5 | I2CSL_SDI_MISO | RXD4 | SCL4 |
| GPIO10 | SPI0_MOSI  | SD2 | DPI_D6 | I2CSL_SDA_MOSI | CTS4 | SDA5 |
| GPIO11 | SPI0_SCLK  | SD3 | DPI_D7 | I2CSL_SCL_SCLK | RTS4 | SCL5 |

## GPIO Libraries

### `raspberry-gpio-python` (a.k.a. `RPi.GPIO`)

- sourceforge.net
  - [raspberry-gpio-python](https://sourceforge.net/projects/raspberry-gpio-python/)
    - [source/](https://sourceforge.net/p/raspberry-gpio-python/code/ci/default/tree/source/)
      - [c_gpio.c](https://sourceforge.net/p/raspberry-gpio-python/code/ci/default/tree/source/c_gpio.c)
        - // try /dev/gpiomem first - this does not require root privs
        - `mem_fd = open("/dev/gpiomem", O_RDWR|O_SYNC)`
          - `gpio_map = (uint32_t *)mmap(NULL, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, 0)`
        - // revert to /dev/mem method - requires root
        - `mem_fd = open("/dev/mem", O_RDWR|O_SYNC)`
          - `gpio_map = (uint32_t *)mmap((void *)gpio_mem, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_FIXED, mem_fd, gpio_base)`

## `pigpio`

- github.com
  - [joan2937/pigpio](<https://github.com/joan2937/pigpio>)
    - [pigpio.c](<https://github.com/joan2937/pigpio/blob/master/pigpio.c>)
      - `fdMem = open("/dev/mem", O_RDWR | O_SYNC)`
        - `gpioReg = initMapMem(fdMem, GPIO_BASE, GPIO_LEN);`
          - `mmap(0, len, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_LOCKED, fd, addr);`
