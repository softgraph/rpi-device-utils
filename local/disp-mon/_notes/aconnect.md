# ALSA sequencer connection manager (`aconnect`)

## References

### USB Specifications

- usb.org
  - USB Device Class Definition for Audio Devices
      <https://www.usb.org/sites/default/files/audio10.pdf>
  - USB Device Class Definition for MIDI Devices
      <https://www.usb.org/sites/default/files/midi10.pdf>
  - USB Device Class Definition for MIDI Devices, Version 2.0
      <https://www.usb.org/sites/default/files/USB%20MIDI%20v2_0.pdf>

## USB Audio Device

### `lsusb`

- You can use `lsusb` and `lsusb -t` command to see which USB devices and interfaces are available.
- A USB MIDI device can be seen as a USB "Audio" class device which has at least two "AudioControl (AC)" and "MIDIStreaming (MS)" interfaces.
- Examples:

```shell
$ lsusb | sort
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 05e3:0608 Genesys Logic, Inc. Hub
Bus 001 Device 003: ID 09e8:1049 AKAI  Professional M.I. Corp. MPK mini 3
Bus 001 Device 004: ID 7104:1400 CME (Central Music Co.) U2MIDI Pro
Bus 001 Device 005: ID 0582:0168 Roland Corp. UM-ONE

$ lsusb -t
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=dwc_otg/1p, 480M
    |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/4p, 480M
        |__ Port 2: Dev 3, If 0, Class=Human Interface Device, Driver=usbhid, 12M
        |__ Port 2: Dev 3, If 1, Class=Audio, Driver=snd-usb-audio, 12M
        |__ Port 2: Dev 3, If 2, Class=Audio, Driver=snd-usb-audio, 12M
        |__ Port 3: Dev 4, If 0, Class=Audio, Driver=snd-usb-audio, 12M
        |__ Port 3: Dev 4, If 1, Class=Audio, Driver=snd-usb-audio, 12M
        |__ Port 4: Dev 5, If 1, Class=Audio, Driver=snd-usb-audio, 12M
        |__ Port 4: Dev 5, If 0, Class=Audio, Driver=snd-usb-audio, 12M
```

| Bus     | Device     | I/F      | Description |
|---------|------------|----------|-------------|
| Bus 001 | Device 003 | If 1 & 2 | AKAI  Professional M.I. Corp. MPK mini 3 |
| Bus 001 | Device 004 | If 0 & 1 | CME (Central Music Co.) U2MIDI Pro |
| Bus 001 | Device 005 | If 0 & 1 | Roland Corp. UM-ONE |

## USB Midi Device

### `aconnect`

- ALSA sequencer connection manager (`aconnect`) is a utility to connect and disconnect two existing ports on ALSA sequencer system.
- You can use `aconnect -l` command to see which MIDI devices and ports are available.

- Example:

```shell
$ aconnect -l
client 0: 'System' [type=kernel]
    0 'Timer           '
    1 'Announce        '
client 14: 'Midi Through' [type=kernel]
    0 'Midi Through Port-0'
client 20: 'MPK mini 3' [type=kernel,card=1]
    0 'MPK mini 3 MIDI 1'
        Connecting To: 24:0
client 24: 'U2MIDI Pro' [type=kernel,card=2]
    0 'U2MIDI Pro MIDI 1'
        Connected From: 20:0
client 28: 'UM-ONE' [type=kernel,card=3]
    0 'UM-ONE MIDI 1   '
```

### `aconnect_ex`

- You can use `local/disp-mon/aconnect_ex` command to see the summary of input/output devices.

- Example:

```shell
$ ~/local/disp-mon/aconnect_ex
# Dev: Device
# In:  Device's Input Port
# Out: Device's Output Port
# Src: Connected Source Port
# Dst: Connected Destination Port
# Con: Connected Devices
Dev 0   'System' [type=kernel]
In  0:0 'System:0' 'Timer           '
In  0:1 'System:1' 'Announce        '
Dev 14   'Midi Through' [type=kernel]
In  14:0 'Midi Through:0' 'Midi Through Port-0'
Out 14:0 'Midi Through:0' 'Midi Through Port-0'
Dev 20   'MPK mini 3' [type=kernel,card=1]
In  20:0 'MPK mini 3:0' 'MPK mini 3 MIDI 1'
Out 20:0 'MPK mini 3:0' 'MPK mini 3 MIDI 1'
Src 20:0 -> 24:0
Dev 24   'U2MIDI Pro' [type=kernel,card=2]
In  24:0 'U2MIDI Pro:0' 'U2MIDI Pro MIDI 1'
Out 24:0 'U2MIDI Pro:0' 'U2MIDI Pro MIDI 1'
Dst 24:0 <- 20:0
Dev 28   'UM-ONE' [type=kernel,card=3]
In  28:0 'UM-ONE:0' 'UM-ONE MIDI 1   '
Out 28:0 'UM-ONE:0' 'UM-ONE MIDI 1   '
Con 'MPK mini 3:0' -> 'U2MIDI Pro:0'
```
