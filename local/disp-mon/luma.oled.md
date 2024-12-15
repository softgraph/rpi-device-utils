# Python Module `luma.oled`

## References

- Luma.OLED
  - readthedocs.io
    - [Luma.OLED](<https://luma-oled.readthedocs.io/en/latest/index.html>)
    - [luma.oled.device](<https://luma-oled.readthedocs.io/en/latest/api-documentation.html>)
    - [luma.oled.device.ssd1306](<https://luma-oled.readthedocs.io/en/latest/api-documentation.html#luma.oled.device.ssd1306>)
  - github.com
    - [luma.oled](<https://github.com/rm-hull/luma.oled>)
    - [luma.examples](<https://github.com/rm-hull/luma.examples>)
    - [luma.examples/examples/demo_opts.py](<https://github.com/rm-hull/luma.examples/blob/main/examples/demo_opts.py>)
  - pypi.org
    - [luma.oled](<https://pypi.org/project/luma.oled/>)

- Luma.Core
  - readthedocs.io
    - [Luma.Core](<https://luma-core.readthedocs.io/en/latest/index.html>)
    - [luma.core.interface.serial](<https://luma-core.readthedocs.io/en/latest/interface.html>)
    - [luma.core.interface.serial.i2c](<https://luma-core.readthedocs.io/en/latest/interface.html#luma.core.interface.serial.i2c>)
    - [luma.core.interface.serial.spi](<https://luma-core.readthedocs.io/en/latest/interface.html#luma.core.interface.serial.spi>)
  - pypi.org
    - [luma.core](<https://pypi.org/project/luma.core/>)

- Pillow
  - readthedocs.io
    - [Pillow](<https://pillow.readthedocs.io/en/stable/>)
      - [Basic Installation](<https://pillow.readthedocs.io/en/stable/installation/basic-installation.html>)
      - [External Libraries](<https://pillow.readthedocs.io/en/stable/installation/building-from-source.html#external-libraries>)
  - pypi.org
    - [pillow](<https://pypi.org/project/pillow/>)

## Preparation

### Required Apt Packages

```shell
$ sudo apt install -y python3-dev python3-setuptools
:
$ sudo apt install -y zlib1g-dev libjpeg-dev libfreetype6-dev
:
```

- External Libraries required by `Pillow`:
  - The following libraries are mandatory.
    - `zlib`
    - `libjpeg`
  - The following library is required for font rendering.
    - `libfreetype`

### Required Python Modules

```shell
$ python3 -m venv ~/venv/disp-mon
:
$ ~/venv/disp-mon/bin/python -m pip install --upgrade pip
:
$ ~/venv/disp-mon/bin/python -m pip install --upgrade Pillow
:
$ ~/venv/disp-mon/bin/python -m pip install --upgrade luma.oled
:
$ ~/venv/disp-mon/bin/python -m pip list
Package    Version
---------- -------
cbor2      5.6.5
luma.core  2.4.2
luma.oled  3.14.0
pillow     11.0.0
pip        24.3.1
pyftdi     0.56.0
pyserial   3.5
pyusb      1.2.1
RPi.GPIO   0.7.1
setuptools 66.1.1
smbus2     0.5.0
spidev     3.6
```

- The versions above are examples.

## Note

### Supported Features of `Pillow`

```shell
$ ~/venv/disp-mon/bin/python -m PIL.report
:
```

- At least, the following features are expected.
  - `PIL CORE`
  - `FREETYPE2`
  - `JPEG`
  - `ZLIB (PNG/ZIP)`

- If `FREETYPE2` is not supported even though `libfreetype` is valid, run the following commands to reconstruct `Pillow`.

```shell
$ ~/venv/disp-mon/bin/python -m pip uninstall -y Pillow
:
$ ~/venv/disp-mon/bin/python -m pip install --no-cache-dir Pillow
:
```
