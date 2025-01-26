#! /usr/bin/env python

#----------------------------------------
# Display Monitor
#
# [USAGE]
# - `python disp_mon.py &`
#----------------------------------------

import os.path

import disp_contents
import disp_device

import event_mon

#----------------------------------------
# Non-public Parameters
#----------------------------------------

_EVENT_QUIT = event_mon.EVENT_QUIT
_EVENT_INCREMENT_AND_DRAW = event_mon.EVENT_COUNT_1000_MS

#----------------------------------------
# Non-public Variables
#----------------------------------------

_context_name = os.path.basename(__file__)

#----------------------------------------
# Non-public Functions
#----------------------------------------

def _main():
    try:
        width = 128
        height = 64
        device = disp_device.configure(_context_name, width, height, 'ssd1309', 'spi')
        disp_contents.init(device, _context_name, width, height)
        event_mon.init(_context_name)
        event_mon.start_cyclic_updater()
        i = 0
        while True:
            event = event_mon.get_event()
            if event == _EVENT_QUIT:
                break
            elif event == _EVENT_INCREMENT_AND_DRAW:
                i = disp_contents.increment_and_draw(i)
    except KeyboardInterrupt:
        pass

#----------------------------------------
# Entry Point
#----------------------------------------

if __name__ == "__main__":
    _main()

#----------------------------------------
