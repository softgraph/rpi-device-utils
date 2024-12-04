#----------------------------------------
# Display Contents
#
# [USAGE]
# - `from disp_contents import monitor`
# - `monitor(device, contextName)`
#----------------------------------------

from collections import deque
import datetime
from glob import iglob
import time

from luma.core.render import canvas # type: ignore

disp_lines = deque([])
disp_temperatures = deque([],maxlen=128)

DURATION_PER_PAGE = 2

def monitor(device, contextName, width, height):
    while True:
        update_disp_lines()
        pages = 0
        if height == 32:
             # the first page contains no line
            LINES_PER_PAGE = 1
            pages = (len(disp_lines) + LINES_PER_PAGE - 1) // LINES_PER_PAGE
            pages += 1  # add the first page
        elif height == 64:
             # the first page contains the first line
            LINES_PER_PAGE = 2
            pages = (len(disp_lines) + LINES_PER_PAGE - 1) // LINES_PER_PAGE
            if pages == 0:
                pages = 1   # the first page with no line
        max = pages * DURATION_PER_PAGE
        for i in range(max):
            update_disp_temperatures()
            with canvas(device) as dc:
                draw_page(dc, i // DURATION_PER_PAGE, width, height) # page: 0, 1, 2, ...
            time.sleep(1)

def update_disp_lines():
    disp_lines.clear()
    for filepath in iglob('/var/tmp/local/disp-mon/*.txt'):
        print(filepath)
        try:
            with open(filepath) as file:
                for line in file:
                    disp_lines.append(line.rstrip())
        except (FileNotFoundError, PermissionError):
            pass

def update_disp_temperatures():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp = int(f.read())
            disp_temperatures.append(temp)
    except (FileNotFoundError, PermissionError):
        pass

def draw_page(dc, page, width, height):
    if height == 32:
        draw_header(dc, 0)              # baseline: 0
        if page == 0:
            draw_temperature_map(dc, 0) # baseline: 0
        else:
            draw_line(dc, 16, page - 1) # baseline: 16, line: 0, 1, 2, ...
    elif height == 64:
        draw_header(dc, 0)              # baseline: 0
        draw_temperature_map(dc, 0)     # baseline: 0
        draw_line(dc, 32, page * 2)     # baseline: 32, line: 0, 2, ...
        draw_line(dc, 48, page * 2 + 1) # baseline: 48, line: 1, 3, ...

def draw_header(dc, baseline):
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    temp = disp_temperatures[-1]
    str_temp = "{:.2f} °C".format(temp / 1000)
    # dc.rectangle(device.bounding_box, outline="white")
    dc.text((85, baseline - 1), str_time, fill="white")
    dc.text(( 0, baseline - 1), str_temp, fill="white")

def draw_temperature_map(dc, baseline):
    x = 0
    for temp in disp_temperatures:
        y = - int(temp / 1000) + 66
        if y < 0:       y = 0
        elif y > 31:    y = 31
        dc.point((x, baseline + y), fill="white")
        x += 1

def draw_line(dc, baseline, line):
    if line >= 0 and line < len(disp_lines):
        dc.text((0, baseline + 5), disp_lines[line], fill="white")

#----------------------------------------
