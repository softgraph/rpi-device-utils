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
disp_temperatures = deque([], maxlen = 128)

DURATION_PER_PAGE = 2

def monitor(device, contextName, width, height):
    while True:
        update_disp_lines()
        page_num = 1
        if height == 32:
            # pages: (No Line), (Line 1). (Line 2), (Line 3), ...
            page_num = count_page_num(line_num = len(disp_lines), line_num_per_page = 1)
            page_num += 1   # add the first page
        elif height == 64:
            # pages: (Line 1, 2), (Line 3, 4), (Line 5, 6), ...
            page_num = count_page_num(line_num = len(disp_lines), line_num_per_page = 2)
            if page_num == 0:
                page_num = 1    # the first page only
        max = page_num * DURATION_PER_PAGE
        for i in range(max):
            update_disp_temperatures()
            with canvas(device) as dc:
                draw_page(dc, width, height, page = i // DURATION_PER_PAGE)
            time.sleep(1)

def count_page_num(line_num, line_num_per_page):
    return (line_num + line_num_per_page - 1) // line_num_per_page

def update_disp_lines():
    disp_lines.clear()
    for filepath in iglob('/var/tmp/local/disp-mon/*.txt'):
        try:
            with open(filepath) as file:
                for line in file:
                    disp_lines.append(line.rstrip())
        except (FileNotFoundError, PermissionError):
            pass

def update_disp_temperatures():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as file:
            temp = int(file.read())
            disp_temperatures.append(temp)
    except (FileNotFoundError, PermissionError):
        pass

def draw_page(dc, width, height, page):
    if height == 32:
        draw_header(dc, base_y = 0)
        if page == 0:
            draw_temperature_map(dc, base_y = 0)
        else:
            draw_line(dc, base_y = 16, line = page - 1)
    elif height == 64:
        draw_header(dc, base_y = 0)
        draw_temperature_map(dc, base_y = 0)
        draw_line(dc, base_y = 32, line = page * 2)
        draw_line(dc, base_y = 48, line = page * 2 + 1)
    else:
        draw_header(dc, base_y = 0)

def draw_header(dc, base_y):
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    temp = disp_temperatures[-1]
    str_temp = "{:.2f} °C".format(temp / 1000)
    # dc.rectangle(device.bounding_box, outline="white")
    dc.text((85, base_y - 1), str_time, fill="white")
    dc.text(( 0, base_y - 1), str_temp, fill="white")

def draw_temperature_map(dc, base_y):
    x = 0
    for temp in disp_temperatures:
        y = - int(temp / 1000) + 66
        if y < 0:
            y = 0
        elif y > 31:
            y = 31
        dc.point((x, base_y + y), fill="white")
        x += 1

def draw_line(dc, base_y, line):
    if line >= 0 and line < len(disp_lines):
        dc.text((0, base_y + 5), disp_lines[line], fill="white")

#----------------------------------------
