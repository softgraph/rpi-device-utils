#! /usr/bin/env python

#----------------------------------------
# MIDI Device Monitor and Automatic Connector
#
# [USAGE]
# - `python midi_mon.py &`
#----------------------------------------

from collections import deque
import logging
import os
import re
import subprocess
import time

from RPi import GPIO # type: ignore

D_DISP_MON = "/var/tmp/local/disp-mon/";
F_DISP_MON = F"{D_DISP_MON}midi_mon.txt";

AUTO_CONNECT_SRC_PORT = "MPK mini 3:0"
AUTO_CONNECT_DST_PORT = "U2MIDI Pro:0"

TICK_TIME_IN_SECONDS = 0.1
TICK_COUNT_DEPRESSED = 2
TICK_COUNT_UPDATE = 10

GPIO_KEYS = [   # Pin #39 = GND
    26,         # Pin #37 = GPIO 26
    19,         # Pin #35 = GPIO 19
    13]         # Pin #33 = GPIO 13
GPIO_KEY_NUM = len(GPIO_KEYS)
GPIO_KEY_TOGGLE_MODE = 1

contextName = os.path.basename(__file__)
logging.basicConfig(format = "%(message)s", level = logging.INFO) # configure handler
logger = logging.getLogger()

gpio_initialized = False

midi_src_ports = deque([])
midi_dst_ports = deque([])
midi_con_pairs = deque([])

def main():
    try:
        monitor()
    except KeyboardInterrupt:
        pass
    finally:
        finalize_gpio()

def initialize_gpio():
    global gpio_initialized
    try:
        GPIO.setmode(GPIO.BCM)
        for key in GPIO_KEYS:
            GPIO.setup(key, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        gpio_initialized = True
        logger.info(f"{contextName}: GPIO is initialized")
        time.sleep(0.1)
    except:
        pass

def finalize_gpio():
    global gpio_initialized
    if gpio_initialized:
        for key in GPIO_KEYS:
            GPIO.cleanup(key)
    gpio_initialized = False
    logger.info(f"{contextName}: GPIO is finalized")

def read_gpio_keys():
    global gpio_initialized
    gpio_keys = [False] * GPIO_KEY_NUM
    if not gpio_initialized:
        initialize_gpio()
    if gpio_initialized:
        for i in range(GPIO_KEY_NUM):
            gpio_keys[i] = not GPIO.input(GPIO_KEYS[i]) # True if pressed
    return gpio_keys

def monitor():
    is_active = True
    pressed_count = [0] * GPIO_KEY_NUM
    idle_count = 0
    while True:
        # Read GPIO Keys
        gpio_keys = read_gpio_keys()

        # Update Key Pressed Counts
        if len(gpio_keys) == GPIO_KEY_NUM:
            for i in range(GPIO_KEY_NUM):
                if gpio_keys[i]:
                    pressed_count[i] += 1
                elif pressed_count[i] > 0:
                    pressed_count[i] = 0

        # Handle Key Depressed (Toggle Mode)
        if pressed_count[GPIO_KEY_TOGGLE_MODE] == TICK_COUNT_DEPRESSED:
            if is_active:
                is_active = False
                deactivate()
                update_inactive()
            else:
                is_active = True
                activate()
                update_active()
            idle_count = 0

        # Handle Update
        elif idle_count >= TICK_COUNT_UPDATE:
            if is_active:
                update_active()
            else:
                update_inactive()
            idle_count = 0

        time.sleep(TICK_TIME_IN_SECONDS)
        idle_count += 1

def deactivate():
    logger.info(f"{contextName}: MIDI Monitor is deactivated")
    disconnect_midi()

def activate():
    logger.info(f"{contextName}: MIDI Monitor is activated")
    pass

def update_inactive():
    try:
        os.makedirs(D_DISP_MON, exist_ok = True)
        with open(F_DISP_MON, "w") as file:
            file.write('MIDI: Disabled')
    except (FileNotFoundError, PermissionError):
        pass

def update_active():
    update_midi()
    connected = False
    for pair in midi_con_pairs:
        if pair[0] == AUTO_CONNECT_SRC_PORT and pair[1] == AUTO_CONNECT_DST_PORT:
            connected = True
            break
    if not connected:
        connect_midi(AUTO_CONNECT_SRC_PORT, AUTO_CONNECT_DST_PORT)
    try:
        os.makedirs(D_DISP_MON, exist_ok = True)
        with open(F_DISP_MON, 'w') as file:
            for pair in midi_con_pairs:
                file.write(f"{pair[0]}  >>>\n")
                file.write(f"\t\t>>>  {pair[1]}\n")
    except (FileNotFoundError, PermissionError):
        pass

def disconnect_midi(disconnect_all = True):
    if disconnect_all:
        logger.info(f"{contextName}: Run `aconnect -x`")
        subprocess.run(["aconnect", "-x"])
        update_midi()

def connect_midi(src_port, dst_port):
    src_valid = False
    dst_valid = False
    for port in midi_src_ports:
        if port == src_port:
            src_valid = True
            break
    for port in midi_dst_ports:
        if port == dst_port:
            dst_valid = True
            break
    if src_valid and dst_valid:
        logger.info(f"{contextName}: Run `aconnect '{src_port}' '{dst_port}'`")
        subprocess.run(["aconnect", f"{src_port}", f"{dst_port}"])
        update_midi()

def update_midi():
    midi_src_ports.clear()
    midi_dst_ports.clear()
    midi_con_pairs.clear()
    try:
        process = subprocess.run(["./aconnect_ex"], check = True, text = True, stdout = subprocess.PIPE)
        for line in process.stdout.splitlines():
            match = re.match(r"""
                             ^ Out          # keyword
                             \s+ (.+:.+)    # #1: device number + port number
                             \s+ '(.+)'     # #2: device name + port number
                             \s+ '(.+)'     # #3: port name
                             $
                             """, line, re.X)
            if match:
                midi_src_ports.append(match.group(2))
            match = re.match(r"""
                             ^ In           # keyword
                             \s+ (.+:.+)    # #1: device number + port number
                             \s+ '(.+)'     # #2: device name + port number
                             \s+ '(.+)'     # #3: port name
                             $
                             """, line, re.X)
            if match:
                midi_dst_ports.append(match.group(2))
            match = re.match(r"""
                             ^ Con          # keyword
                             \s+ '(.+)'     # #1: source device and port
                             \s+ ->         # keyword
                             \s+ '(.+)'     # #2: destination device and port
                             $
                             """, line, re.X)
            if match:
                midi_con_pairs.append([ match.group(1), match.group(2) ])
    except (subprocess.CalledProcessError):
        pass

if __name__ == "__main__":
    main()

#----------------------------------------
