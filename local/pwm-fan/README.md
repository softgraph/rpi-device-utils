# `pwm-fan`

## Setup

- `pwm-fan.dtbo` is a device tree blob for overlay (DTBO) to control the speed of a cooling fan using PWM.
- To setup `pwm-fan.dtbo` on the device, see:
  - [rpi_setup_pwm_fan.sh](../../rpi_setup_pwm_fan.sh)

## Source Code

- Here are examples. They are almost the same except for parameters.
  - 3-pin PWM Fan connected to 5V, GND and GPIO 18 (PWM0 or PWM0_0)
    - [pwm-fan.rpi-2.local.dts](./pwm-fan.rpi-2.local.dts)
    - [pwm-fan.rpi-3.local.dts](./pwm-fan.rpi-3.local.dts)
    - [pwm-fan.rpi-4.local.dts](./pwm-fan.rpi-4.local.dts)

## Technical Notes

- [Device Tree](<Device Tree.md>)
- [Thermal Management](<Thermal Management.md>)
- [GPIO](<../../Raspberry Pi/gpio.md>)
