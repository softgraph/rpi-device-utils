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
TICK_COUNT_UPDATE = 5

GPIO_KEY_0 = 26
GPIO_KEY_1 = 19
GPIO_KEY_2 = 13
GPIO_KEY = GPIO_KEY_1

contextName = os.path.basename(__file__)
logging.basicConfig(format = '%(levelname)s, %(message)s', level = logging.INFO)
logger = logging.getLogger()

gpio_key = 0

midi_src_ports = deque([])
midi_dst_ports = deque([])
midi_con_pairs = deque([])

def main():
    try:
        monitor(contextName)
    except KeyboardInterrupt:
        pass
    finally:
        finalize_gpio()

def initialize_gpio():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_KEY, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        global gpio_key
        gpio_key = GPIO_KEY
        logger.info(f"[{contextName}] GPIO, initialized")
        time.sleep(0.1)
    except:
        pass

def finalize_gpio():
    global gpio_key
    if gpio_key > 0:
        GPIO.cleanup(gpio_key)
    gpio_key = 0
    logger.info(f"[{contextName}] GPIO, finalized")

def read_gpio_key():
    # returns True if pressed
    if gpio_key == 0:
        initialize_gpio()
    if gpio_key > 0:
        return not GPIO.input(gpio_key)
    else:
        return False

def monitor(contextName):
    is_active = True
    pressed_count = 0
    idle_count = 0
    while True:
        # Check the State of Key
        if read_gpio_key():
            pressed_count += 1
        elif pressed_count > 0:
            pressed_count = 0

        if pressed_count == TICK_COUNT_DEPRESSED:
            # Handle Depressed Key
            if is_active:
                is_active = False
                deactivate()
                update_inactive()
            else:
                is_active = True
                activate()
                update_active()
            idle_count = 0

        elif idle_count >= TICK_COUNT_UPDATE:
            # Handle Update
            if is_active:
                update_active()
            else:
                update_inactive()
            idle_count = 0

        time.sleep(TICK_TIME_IN_SECONDS)
        idle_count += 1

def deactivate():
    logger.info(f"[{contextName}] Deactivated")
    disconnect_midi()

def activate():
    logger.info(f"[{contextName}] Activated")
    pass

def update_inactive():
    try:
        os.makedirs(D_DISP_MON, exist_ok = True)
        with open(F_DISP_MON, "w") as file:
            file.write('midi-mon: disabled')
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
                file.write(f"{pair[0]} >>>\n")
                file.write(f">>> {pair[1]}\n")
    except (FileNotFoundError, PermissionError):
        pass

def disconnect_midi(disconnect_all = True):
    if disconnect_all:
        logger.info(f"[{contextName}] Run, aconnect, -x")
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
        logger.info(f"[{contextName}] Run, aconnect, '{src_port}', '{dst_port}'")
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
