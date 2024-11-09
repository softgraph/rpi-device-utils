# Luma.OLED

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
  - pypi.org
    - [pillow](<https://pypi.org/project/pillow/>)

## Preparation

### Required Apt Packages

```shell
$ sudo apt install -y python3-dev
:
$ sudo apt install -y libjpeg-dev
:
$ sudo apt install -y zlib1g-dev
:
```

### Required Pip Packages

```shell
$ python3 -m venv ~/venv/luma
:
$ ~/venv/luma/bin/python -m pip install --upgrade pip
:
$ ~/venv/luma/bin/python -m pip install --upgrade Pillow
:
$ ~/venv/luma/bin/python -m pip install --upgrade luma.oled
:
```
