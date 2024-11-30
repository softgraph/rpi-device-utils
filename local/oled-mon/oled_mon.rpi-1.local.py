#! /usr/bin/env python

#----------------------------------------
# OLED Monitor
#
# [USAGE]
# - `python oled_mon.py &`
#----------------------------------------

from collections import deque
import datetime
import os.path
import time

from oled_ssd1306_i2c import configure_device
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
    count_plane_0 = 3
    count_plane_1 = count_plane_0 * 2
    i = 0
    while True:
        update()
        with canvas(device) as dc:
            draw_common(dc)
            if i < count_plane_0:
                draw_plane_0(dc)
            elif i < count_plane_1:
                draw_plane_1(dc)
        i += 1
        if i >= count_plane_1:
            i = 0
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

def draw_plane_1(dc):
    str_midi = ''
    try:
        with open('/var/tmp/local/midi-con.txt') as fc:
            str_midi = fc.readline().rstrip()
    except (FileNotFoundError, PermissionError):
        pass
    if len(str_midi) > 0:
        dc.text((0, 21), str_midi, fill="white")
    else:
        draw_plane_0(dc)

#----------------------------------------

if __name__ == "__main__":
    main()

#----------------------------------------
