# `midi-mon`

## Setup

- `midi_mon.sh` is a shell script to periodically check the connection between two midi devices.
- To setup `midi_mon.sh` on the device, see:
  - [rpi_setup_midi_mon.sh](../../rpi_setup_midi_mon.sh)

## Source Code

- Here is an example.
  - [midi_mon.rpi-1.local.sh](midi_mon.rpi-1.local.sh)

## Technical Notes

### USB Audio Device

- You can use `lsusb` and `lsusb -t` command to see which USB devices and interfaces are available.
- A USB MIDI device can be seen as a USB "Audio" class device which has at least two "AudioControl (AC)" and "MIDIStreaming (MS)" interfaces.

### USB Midi Device

- You can use `aconnect -l` command to see which MIDI devices and ports are available.

### USB Specifications

- Refer to:
  - usb.org
    - USB Device Class Definition for Audio Devices
      <https://www.usb.org/sites/default/files/audio10.pdf>
    - USB Device Class Definition for MIDI Devices
      <https://www.usb.org/sites/default/files/midi10.pdf>
    - USB Device Class Definition for MIDI Devices, Version 2.0
      <https://www.usb.org/sites/default/files/USB%20MIDI%20v2_0.pdf>
