#----------------------------------------
# Event Monitor
#
# [USAGE]
# - `import event_mon`
# - `event_mon.init(_context_name)`
# - `event_mon.start_cyclic_updater()`
# - `while True:`
# - `    event = event_mon.get_event()`
# - `    :`
#----------------------------------------

import logging
import queue
import threading
import time

from RPi import GPIO # type: ignore

#----------------------------------------
# Public Constants
#----------------------------------------

EVENT_QUIT = 0
EVENT_COUNT_300_MS = 3
EVENT_COUNT_1000_MS = 10
EVENT_GPO_KEY_DEPRESSED_0 = 100

#----------------------------------------
# Non-public Parameters
#----------------------------------------

_GPIO_KEYS = [  # Pin #39 = GND
    26,         # Pin #37 = GPIO 26
    19,         # Pin #35 = GPIO 19
    13          # Pin #33 = GPIO 13
]

_GPIO_KEY_NUM = len(_GPIO_KEYS)

_TICK_DURATION_IN_SECONDS = 0.1
_TICK_COUNT_GPIO_KEY_DEPRESSED = 2
_TICK_COUNT_300_MS = 3
_TICK_COUNT_1000_MS = 10

_GPIO_PAUSE_DURATION_IN_SECONDS = 0.1

#----------------------------------------
# Non-public Variables
#----------------------------------------

_contextName = None

logging.basicConfig(format = "%(message)s", level = logging.INFO) # configure handler
_logger = logging.getLogger()

_event_quit = False
_event_queue = queue.SimpleQueue()

_gpio_initialized = False

#----------------------------------------
# Public Functions
#----------------------------------------

def init(context_name):
    global _context_name
    _context_name = context_name

def quit():
    global _event_quit
    _event_quit = True

def get_event():
    event = _event_queue.get()
    return event

def put_event(event):
    _event_queue.put(event)

def start_cyclic_updater():
    thread = threading.Thread(target=_cyclic_updater)
    thread.start()

def start_cyclic_updater_with_gpio_keys():
    thread = threading.Thread(target=_cyclic_updater_with_gpio_keys)
    thread.start()

#----------------------------------------
# Non-public Functions
#----------------------------------------

def _cyclic_updater():
    while True:
        # Sleep
        time.sleep(_TICK_DURATION_IN_SECONDS * _TICK_COUNT_1000_MS)

        # Check quit flag
        if _event_quit:
            _event_queue.put(EVENT_QUIT)
            break

        # Handle Count Event (1000 ms)
        _event_queue.put(EVENT_COUNT_1000_MS)

def _cyclic_updater_with_gpio_keys():
    tick_count_1000_ms = 0
    tick_count_300_ms = 0
    pressed_count = [0] * _GPIO_KEY_NUM
    while True:
        # Sleep
        time.sleep(_TICK_DURATION_IN_SECONDS)

        # Check quit flag
        if _event_quit:
            _event_queue.put(EVENT_QUIT)
            break

        # Read GPIO Keys
        gpio_keys = _read_gpio_keys()

        # Update Key Pressed Counts
        if len(gpio_keys) == _GPIO_KEY_NUM:
            for i in range(_GPIO_KEY_NUM):
                if gpio_keys[i]:
                    pressed_count[i] += 1
                elif pressed_count[i] > 0:
                    pressed_count[i] = 0

        # Handle GPIO Key Depressed Event
        for i in range(_GPIO_KEY_NUM):
            if pressed_count[i] >= _TICK_COUNT_GPIO_KEY_DEPRESSED:
                _event_queue.put(EVENT_GPO_KEY_DEPRESSED_0 + i)

        # Handle Count Event (1000 ms)
        if tick_count_1000_ms >= _TICK_COUNT_1000_MS:
            _event_queue.put(EVENT_COUNT_1000_MS)
            tick_count_1000_ms = 0
        tick_count_1000_ms += 1

        # Handle Count Event (300 ms)
        if tick_count_300_ms >= _TICK_COUNT_300_MS:
            _event_queue.put(EVENT_COUNT_300_MS)
            tick_count_300_ms = 0
        tick_count_300_ms += 1

    _finalize_gpio()

def _read_gpio_keys():
    global _gpio_initialized
    gpio_keys = [False] * _GPIO_KEY_NUM
    if not _gpio_initialized:
        _initialize_gpio()
    if _gpio_initialized:
        for i in range(_GPIO_KEY_NUM):
            gpio_keys[i] = not GPIO.input(_GPIO_KEYS[i]) # True if pressed
    return gpio_keys

def _initialize_gpio():
    global _gpio_initialized
    if _gpio_initialized:
        return
    try:
        GPIO.setmode(GPIO.BCM)
        for key in _GPIO_KEYS:
            GPIO.setup(key, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        _gpio_initialized = True
        _logger.info(f"{_contextName}: GPIO is initialized")
        time.sleep(_GPIO_PAUSE_DURATION_IN_SECONDS)
    except:
        pass

def _finalize_gpio():
    global _gpio_initialized
    if _gpio_initialized:
        for key in _GPIO_KEYS:
            GPIO.cleanup(key)
    _gpio_initialized = False
    _logger.info(f"{_contextName}: GPIO is finalized")

#----------------------------------------
