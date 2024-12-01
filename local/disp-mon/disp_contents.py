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

disp_pages = deque([])
disp_temperatures = deque([],maxlen=128)

def monitor(device, contextName):
    while True:
        COUNT_PER_PAGE = 2
        update_disp_pages()
        pages = len(disp_pages) + 1
        max = COUNT_PER_PAGE * pages
        for i in range(max):
            update_disp_temperatures()
            with canvas(device) as dc:
                draw_page(dc, i // COUNT_PER_PAGE)
            time.sleep(1)

def update_disp_pages():
    disp_pages.clear()
    for filepath in iglob('/var/tmp/local/disp-mon/*.txt'):
        print(filepath)
        try:
            with open(filepath) as file:
                for line in file:
                    disp_pages.append(line.rstrip())
        except (FileNotFoundError, PermissionError):
            pass

def update_disp_temperatures():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp = int(f.read())
            disp_temperatures.append(temp)
    except (FileNotFoundError, PermissionError):
        pass

def draw_common(dc):
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    temp = disp_temperatures[-1]
    str_temp = "{:.2f} °C".format(temp / 1000)
    # dc.rectangle(device.bounding_box, outline="white")
    dc.text((85, -1), str_time, fill="white")
    dc.text(( 0, -1), str_temp, fill="white")

def draw_page(dc, page):
    draw_common(dc)
    if (page > 0):
        dc.text((0, 21), disp_pages[page - 1], fill="white")
    else:
        x = 0
        for temp in disp_temperatures:
            y = - int(temp / 1000) + 66
            if y < 0: y = 0
            elif y > 31: y = 31
            dc.point((x,y), fill="white")
            x += 1

#----------------------------------------
