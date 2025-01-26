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
import midi_mon # type: ignore

#----------------------------------------
# Non-public Parameters
#----------------------------------------

_EVENT_QUIT = event_mon.EVENT_QUIT
_EVENT_INCREMENT_AND_DRAW = event_mon.EVENT_COUNT_1000_MS
_EVENT_UPDATE_AND_DRAW = event_mon.EVENT_COUNT_300_MS
_EVENT_MIDI_TOGGLE = event_mon.EVENT_GPO_KEY_DEPRESSED_0 + 1

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
        device = disp_device.configure(_context_name, width, height, 'ssd1306', 'i2c', clockwise_rotation = 180)
        disp_contents.init(device, _context_name, width, height)
        event_mon.init(_context_name)
        event_mon.start_cyclic_updater_with_gpio_keys()
        midi_mon.init(_context_name)
        i = 0
        while True:
            event = event_mon.get_event()
            if event == _EVENT_QUIT:
                break
            elif event == _EVENT_INCREMENT_AND_DRAW:
                i = disp_contents.increment_and_draw(i)
            elif event == _EVENT_UPDATE_AND_DRAW:
                if midi_mon.update():
                    i = disp_contents.update_and_draw()
            elif event == _EVENT_MIDI_TOGGLE:
                if midi_mon.toggle():
                    i = disp_contents.update_and_draw()
    except KeyboardInterrupt:
        pass

#----------------------------------------
# Entry Point
#----------------------------------------

if __name__ == "__main__":
    _main()

#----------------------------------------
