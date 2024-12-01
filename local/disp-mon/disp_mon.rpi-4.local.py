#! /usr/bin/env python

#----------------------------------------
# Display Monitor
#
# [USAGE]
# - `python oled_mon.py &`
#----------------------------------------

from collections import deque
import datetime
import os.path
import time

from disp_ssd1305_spi import configure_device
from luma.core.render import canvas # type: ignore

contextName = os.path.basename(__file__)
deque_temp = deque([],maxlen=128)

def main():
    try:
        device = configure_device(contextName)
        monitor(device)
    except KeyboardInterrupt:
        pass

def monitor(device):
    while True:
        update()
        with canvas(device) as dc:
            draw_common(dc)
            draw_plane_0(dc)
        time.sleep(1)

def update():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as fc:
            temp = int(fc.read())
            deque_temp.append(temp)
    except (FileNotFoundError, PermissionError):
        pass

def draw_common(dc):
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    temp = deque_temp[-1]
    str_temp = "{:.2f} °C".format(temp / 1000)
    # dc.rectangle(device.bounding_box, outline="white")
    dc.text((85, -1), str_time, fill="white")
    dc.text(( 0, -1), str_temp, fill="white")

def draw_plane_0(dc):
    x = 0
    for temp in deque_temp:
        y = - int(temp / 1000) + 66
        if y < 0: y = 0
        elif y > 31: y = 31
        dc.point((x,y), fill="white")
        x += 1

#----------------------------------------

if __name__ == "__main__":
    main()

#----------------------------------------
