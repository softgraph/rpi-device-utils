#! /usr/bin/env python

#----------------------------------------
# Display Monitor
#
# [USAGE]
# - `python disp_mon.py &`
#----------------------------------------

import os.path

from disp_contents import monitor
from disp_device import configure_device

contextName = os.path.basename(__file__)

def main():
    try:
        width = 128
        height = 64
        device = configure_device(contextName, width, height, 'ssd1309', 'spi')
        monitor(device, contextName, width, height)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

#----------------------------------------
