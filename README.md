# rpi-device-utils

A collection of utilities used to manage Raspberry Pi devices.

## Requirements

### Host

- `bash`
- `ssh`
- `dscacheutil` (for `rpi_show_address.sh` only)

### Target

- Raspberry Pi OS

## Preparation

- Run `. _prepare.sh`.
- Configure each Raspberry Pi device to accept a password-less ssh connection using `ssh user@hostname`.
  - For the details, refer to:
    - raspberrypi.com
      - Raspberry Pi Documentation
        - [Remote access](<https://www.raspberrypi.com/documentation/computers/remote-access.html>)
          - [Configure SSH without a password](<https://www.raspberrypi.com/documentation/computers/remote-access.html#configure-ssh-without-a-password>)
- Create `targets` file as `targets.example`.

## Utilities

- Device's IP Addresses & Ping
  - [`rpi_show_address.sh`](<rpi_show_address.sh>)
  - [`rpi_ping.sh`](<rpi_ping.sh>)
- Device's Status & Information
  - [`rpi_show_status.sh`](<rpi_show_status.sh>)
    - <a href="status.bash">`status.bash/`</a>
  - [`rpi_get_info.sh`](<rpi_get_info.sh>)
    - <a href="info.txt.bash">`info.txt.bash/`</a>
    - <a href="info.csv.bash">`info.csv.bash/`</a>
- Run Command on Device
  - [`rpi_run.sh`](<rpi_run.sh>)
- Setup Device
  - [`rpi_setup_pwm-fan.sh`](<rpi_setup_pwm-fan.sh>)
    - <a href="local/pwm-fan">`local/pwm-fan/`</a>
    - See also:
      - [README.md](<local/pwm-fan/README.md>)
  - [`rpi_setup_oled-mon.sh`](<rpi_setup_oled-mon.sh>)
    - <a href="local/oled-mon">`local/oled-mon/`</a>
    - See also:
      - [README.md](<local/oled-mon/README.md>)
