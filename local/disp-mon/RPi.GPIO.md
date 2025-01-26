# Python Module `RPi.GPIO`

## References

- pypi.org
  - [RPi.GPIO](<https://pypi.org/project/RPi.GPIO/>)
- sourceforge.net
  - [raspberry-gpio-python](<https://sourceforge.net/projects/raspberry-gpio-python/>)
    - [Wiki](<https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/>)
      - [Examples](<https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/>)

## Preparation

### Required Apt Packages

```shell
$ sudo apt install -y python3-dev python3-setuptools
:
```

### Required Python Modules

```shell
$ python3 -m venv ~/venv/midi-mon
:
$ ~/venv/midi-mon/bin/python -m pip install --upgrade pip
:
$ ~/venv/midi-mon/bin/python -m pip install --upgrade RPi.GPIO
:
$ ~/venv/midi-mon/bin/python -m pip list
Package    Version
---------- -------
pip        24.3.1
RPi.GPIO   0.7.1
setuptools 66.1.1
```

- The versions above are examples.
