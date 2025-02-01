# Preparation

## (1) Install Required Apt Packages

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

## (2) Create New Python `venv` for `disp-mon`

```shell
$ python3 -m venv ~/venv/disp-mon
:
```

## (3) Install Required Python Modules

```shell
$ ~/venv/disp-mon/bin/python -m pip install --upgrade pip
:
$ ~/venv/disp-mon/bin/python -m pip install --upgrade Pillow
:
$ ~/venv/disp-mon/bin/python -m pip install --upgrade luma.oled
:
$ ~/venv/disp-mon/bin/python -m pip install --upgrade RPi.GPIO
:
$ ~/venv/disp-mon/bin/python -m pip install --upgrade pyserial
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

### Verify Supported Features of `Pillow`

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
