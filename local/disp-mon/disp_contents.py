#----------------------------------------
# Display Contents
#
# [USAGE]
# - `import disp_contents`
# - `import time`
# - `disp_contents.init(device, context_name, width, height)`
# - `i = 0`
# - `while True:`
# - `    i = disp_contents.update_and_draw(i)`
# - `    time.sleep(1)`
#----------------------------------------

import collections
import datetime
from glob import iglob

from luma.core.render import canvas # type: ignore
from PIL import ImageFont # type: ignore

#----------------------------------------
# Non-public Parameters
#----------------------------------------

_DURATION_PER_PAGE = 2

#----------------------------------------
# Non-public Constants
#----------------------------------------

_TEXT_ALIGN_LEFT = 0
_TEXT_ALIGN_CENTER = 1
_TEXT_ALIGN_RIGHT = 2

_TEXT_VALIGN_TOP = 0
_TEXT_VALIGN_CENTER = 1
_TEXT_VALIGN_BOTTOM = 2

#----------------------------------------
# Non-public Variables
#----------------------------------------

_device = None
_context_name = None
_page_width = None
_page_height = None
_bounding_box = None
_default_font = None

_disp_lines = collections.deque([])
_disp_temperatures = collections.deque([], maxlen = 128)

_max = 0

#----------------------------------------
# Public Functions
#----------------------------------------

def init(device, context_name, width, height):
    global _device
    global _context_name
    global _page_width
    global _page_height
    global _bounding_box
    global _default_font
    _device = device
    _context_name = context_name
    _page_width = width
    _page_height = height
    _bounding_box = device.bounding_box
    _default_font = ImageFont.load_default()

# Increment & Draw Contents Periodically
def increment_and_draw(i):
    if _max == 0 or i == 0:
        _refresh_pages()
    _update_disp_temperatures()
    draw(i)
    i += 1
    if i >= _max:
        i = 0
    return i

# Update & Draw Contents
def update_and_draw():
    _refresh_pages()
    i = 0
    draw(i)
    return i

# Draw Contents
def draw(i):
    with canvas(_device) as dc:
        _draw_page(dc, page = i // _DURATION_PER_PAGE)

#----------------------------------------
# Non-public Functions
#----------------------------------------

def _count_page_num(line_num, line_num_per_page):
    return (line_num + line_num_per_page - 1) // line_num_per_page

def _refresh_pages():
    global _max
    _update_disp_lines()
    page_num = 1
    if _page_height == 32:
        # pages: (No Line), (Line 1). (Line 2), (Line 3), ...
        page_num = _count_page_num(line_num = len(_disp_lines), line_num_per_page = 1)
        page_num += 1   # add the first page
    elif _page_height == 64:
        # pages: (Line 1, 2), (Line 3, 4), (Line 5, 6), ...
        page_num = _count_page_num(line_num = len(_disp_lines), line_num_per_page = 2)
        if page_num == 0:
            page_num = 1    # the first page only
    _max = page_num * _DURATION_PER_PAGE

def _update_disp_lines():
    _disp_lines.clear()
    for filepath in iglob('/var/tmp/local/disp-mon/*.txt'):
        try:
            with open(filepath) as file:
                for line in file:
                    line = line.rstrip()
                    if len(line) > 0:
                        _disp_lines.append(line)
        except (FileNotFoundError, PermissionError):
            pass

def _update_disp_temperatures():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as file:
            temp = int(file.read())
            _disp_temperatures.append(temp)
    except (FileNotFoundError, PermissionError):
        pass

def _draw_page(dc, page):
    if _page_height == 32:
        _draw_header(dc, _page_width, base_y = 0)
        if page == 0:
            _draw_temperature_map(dc, _page_width, base_y = 0)
        else:
            _draw_line(dc, _page_width, base_y = 16, index = page - 1)
    elif _page_height == 64:
        _draw_header(dc, _page_width, base_y = 0)
        _draw_temperature_map(dc, _page_width, base_y = 0)
        _draw_line(dc, _page_width, base_y = 32, index = page * 2)
        _draw_line(dc, _page_width, base_y = 48, index = page * 2 + 1)
    else:
        _draw_header(dc, _page_width, base_y = 0)

def _draw_header(dc, width, base_y):
    # Draw Rectangle
    # dc.rectangle(_bounding_box, outline = "white")

    # Draw Temperature
    if len(_disp_temperatures) > 0:
        temp = _disp_temperatures[-1]
        str_temp = "{:.2f} °C".format(temp / 1000)
    else:
        str_temp = ""
    _draw_text(dc, width, base_y, str_temp, _TEXT_ALIGN_LEFT, _TEXT_VALIGN_TOP)

    # Draw Time
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    _draw_text(dc, width, base_y, str_time, _TEXT_ALIGN_RIGHT, _TEXT_VALIGN_TOP)

def _draw_temperature_map(dc, width, base_y):
    x = 0
    for temp in _disp_temperatures:
        y = - int(temp / 1000) + 66
        if y < 0:
            y = 0
        elif y > 31:
            y = 31
        dc.point((x, base_y + y), fill="white")
        x += 1

def _draw_line(dc, width, base_y, index):
    if index >= 0 and index < len(_disp_lines):
        line = _disp_lines[index]
        if len(line) > 1 and line[0] == "\t":
            if len(line) > 2 and line[1] == "\t":
                line = line.lstrip()
                _draw_text(dc, width, base_y, line, _TEXT_ALIGN_RIGHT, _TEXT_VALIGN_BOTTOM)
            else:
                line = line.lstrip()
                _draw_text(dc, width, base_y, line, _TEXT_ALIGN_CENTER, _TEXT_VALIGN_BOTTOM)
        else:
            _draw_text(dc, width, base_y, line, _TEXT_ALIGN_LEFT, _TEXT_VALIGN_BOTTOM)

def _draw_text(dc, width, base_y, text, align, valigh):
    if align == _TEXT_ALIGN_RIGHT:
        font_width = _default_font.getlength(text)
        font_width += len(text) * 0.25 # magic
        x = (width - font_width) // 1
    elif align == _TEXT_ALIGN_CENTER:
        font_width = _default_font.getlength(text)
        font_width += len(text) * 0.25 # magic
        x = (width - font_width) // 2
    else:
        x = 0
    if valigh == _TEXT_VALIGN_BOTTOM:
        y = base_y + 5
    elif valigh == _TEXT_VALIGN_CENTER:
        y = base_y + 2
    else:
        y = base_y - 1
    dc.text((x, y), text, fill = "white", font = _default_font)

#----------------------------------------
