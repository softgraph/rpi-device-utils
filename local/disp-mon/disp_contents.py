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
from PIL import ImageFont # type: ignore

DURATION_PER_PAGE = 2

TEXT_ALIGN_LEFT = 0
TEXT_ALIGN_CENTER = 1
TEXT_ALIGN_RIGHT = 2

TEXT_VALIGN_TOP = 0
TEXT_VALIGN_CENTER = 1
TEXT_VALIGN_BOTTOM = 2

disp_lines = deque([])
disp_temperatures = deque([], maxlen = 128)

bounding_box = None
default_font = None

def load_defaults(device):
    global bounding_box
    global default_font
    if bounding_box == None:
        bounding_box = device.bounding_box
    if default_font == None:
        default_font = ImageFont.load_default()

def monitor(device, contextName, width, height):
    load_defaults(device)
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
                    line = line.rstrip()
                    if len(line) > 0:
                        disp_lines.append(line)
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
        draw_header(dc, width, base_y = 0)
        if page == 0:
            draw_temperature_map(dc, width, base_y = 0)
        else:
            draw_line(dc, width, base_y = 16, index = page - 1)
    elif height == 64:
        draw_header(dc, width, base_y = 0)
        draw_temperature_map(dc, width, base_y = 0)
        draw_line(dc, width, base_y = 32, index = page * 2)
        draw_line(dc, width, base_y = 48, index = page * 2 + 1)
    else:
        draw_header(dc, width, base_y = 0)

def draw_header(dc, width, base_y):
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    temp = disp_temperatures[-1]
    str_temp = "{:.2f} °C".format(temp / 1000)
    # dc.rectangle(bounding_box, outline = "white")
    draw_text(dc, width, base_y, str_temp, TEXT_ALIGN_LEFT, TEXT_VALIGN_TOP)
    draw_text(dc, width, base_y, str_time, TEXT_ALIGN_RIGHT, TEXT_VALIGN_TOP)

def draw_temperature_map(dc, width, base_y):
    x = 0
    for temp in disp_temperatures:
        y = - int(temp / 1000) + 66
        if y < 0:
            y = 0
        elif y > 31:
            y = 31
        dc.point((x, base_y + y), fill="white")
        x += 1

def draw_line(dc, width, base_y, index):
    if index >= 0 and index < len(disp_lines):
        line = disp_lines[index]
        if len(line) > 1 and line[0] == "\t":
            if len(line) > 2 and line[1] == "\t":
                line = line.lstrip()
                draw_text(dc, width, base_y, line, TEXT_ALIGN_RIGHT, TEXT_VALIGN_BOTTOM)
            else:
                line = line.lstrip()
                draw_text(dc, width, base_y, line, TEXT_ALIGN_CENTER, TEXT_VALIGN_BOTTOM)
        else:
            draw_text(dc, width, base_y, line, TEXT_ALIGN_LEFT, TEXT_VALIGN_BOTTOM)

def draw_text(dc, width, base_y, text, align, valigh):
    if align == TEXT_ALIGN_RIGHT:
        font_width = default_font.getlength(text)
        font_width += len(text) * 0.25 # magic
        x = (width - font_width) // 1
    elif align == TEXT_ALIGN_CENTER:
        font_width = default_font.getlength(text)
        font_width += len(text) * 0.25 # magic
        x = (width - font_width) // 2
    else:
        x = 0
    if valigh == TEXT_VALIGN_BOTTOM:
        y = base_y + 5
    elif valigh == TEXT_VALIGN_CENTER:
        y = base_y + 2
    else:
        y = base_y - 1
    dc.text((x, y), text, fill = "white", font = default_font)

#----------------------------------------
