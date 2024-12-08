# Raspberry Pi Device Utilities (`rpi-device-utils`)

A collection of utilities used to manage Raspberry Pi devices.

## Requirements

### Host

- `bash`
- `ssh`

### Target

- Raspberry Pi OS

## Preparation

- Run [`. _prepare.sh`](<_prepare.sh>).
- Configure each Raspberry Pi device to accept a password-less ssh connection using `ssh user@hostname`.
  - For the details, refer to:
    - raspberrypi.com
      - Raspberry Pi Documentation
        - [Remote access](<https://www.raspberrypi.com/documentation/computers/remote-access.html>)
          - [Configure SSH without a password](<https://www.raspberrypi.com/documentation/computers/remote-access.html#configure-ssh-without-a-password>)
- Create `targets` file as [`targets.example`](<targets.example>).

## Utilities

- Device's IP Addresses
  - [`rpi_show_address.sh`](<rpi_show_address.sh>)
- Device's Status & Information
  - [`rpi_show_status.sh`](<rpi_show_status.sh>)
    - <a href="status.bash">`status.bash/`</a>
  - [`rpi_get_info.sh`](<rpi_get_info.sh>)
    - <a href="info.txt.bash">`info.txt.bash/`</a>
    - <a href="info.csv.bash">`info.csv.bash/`</a>
- Run Command on Device
  - [`rpi_run.sh`](<rpi_run.sh>)
- Setup Device
  - [Display Monitor (`disp-mon`)](<local/disp-mon/README.md>)
    - [`rpi_setup_disp_mon.sh`](<rpi_setup_disp_mon.sh>)
      - <a href="local/disp-mon">`local/disp-mon/`</a>
  - [MIDI Monitor (`midi-mon`)](<local/midi-mon/README.md>)
    - [`rpi_setup_midi_mon.sh`](<rpi_setup_midi_mon.sh>)
      - <a href="local/midi-mon">`local/midi-mon/`</a>
  - [PWM Fan (`pwm-fan`)](<local/pwm-fan/README.md>)
    - [`rpi_setup_pwm_fan.sh`](<rpi_setup_pwm_fan.sh>)
      - <a href="local/pwm-fan">`local/pwm-fan/`</a>
