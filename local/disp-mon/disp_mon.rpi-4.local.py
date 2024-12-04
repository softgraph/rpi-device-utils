#! /usr/bin/env python

#----------------------------------------
# Display Monitor
#
# [USAGE]
# - `python disp_mon.py &`
#----------------------------------------

import os.path

from disp_contents import monitor
from disp_ssd1305_spi import configure_device

contextName = os.path.basename(__file__)

def main():
    try:
        width = 128
        height = 32
        device = configure_device(contextName, width, height)
        monitor(device, contextName, width, height)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

#----------------------------------------
