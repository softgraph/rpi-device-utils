# PWM Fan (`pwm-fan`)

## Setup

- `pwm-fan.dtbo` is a device tree blob for overlay (DTBO) to control the speed of a cooling fan using PWM.
- To setup `pwm-fan.dtbo` on the device, see:
  - [rpi_setup_pwm_fan.sh](../../rpi_setup_pwm_fan.sh)

## Source Code Examples

### 3-pin PWM Fan

- [pwm-fan.rpi-2.local.dts](./pwm-fan.rpi-2.local.dts)
- [pwm-fan.rpi-3.local.dts](./pwm-fan.rpi-3.local.dts)
- [pwm-fan.rpi-4.local.dts](./pwm-fan.rpi-4.local.dts)
  - They are almost the same except for parameters.

| Signal | Line  | Pin |
|--------|-------|-----|
| +5V    | Red   | 5V  |
| GND    | Black | GND |
| PWM    | Blue  | GPIO 18 (PWM0 or PWM0_0) |

## GPIO Layout

| Line | Pin    | #  | #  | Pin         | Line |
|------|--------|----|----|-------------|------|
|      | (3.3V) | 1  | 2  | **5V**      | Red  |
|      | -      | 3  | 4  | **5V**      | Red  |
|      | -      | 5  | 6  | **GND**     | Black |
|      | -      | 7  | 8  | -           |      |
|      | (GND)  | 9  | 10 | -           |      |
|      | -      | 11 | 12 | **GPIO 18** | Blue |
|      | -      | 13 | 14 | **GND**     | Black |

- See also:
  - [Raspberry Pi / GPIO](<../../Raspberry Pi/gpio.md>)

## Technical Notes

- [Device Tree](<Device Tree.md>)
- [Thermal Management](<Thermal Management.md>)
- [GPIO](<../../Raspberry Pi/gpio.md>)
