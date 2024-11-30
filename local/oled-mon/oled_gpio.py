#----------------------------------------
# GPIO support for OLED Devices
#
# [USAGE]
# - `from oled_gpio import ensure_gpio_ready`
# - `ensure_gpio_ready()`
#----------------------------------------

import logging
import time

logger = logging.getLogger()

def ensure_gpio_ready(contextName):
    gpiomem = '/dev/gpiomem'
    waiting = False
    while True:
        try:
            with open(gpiomem) as x:
                break
        except (FileNotFoundError, PermissionError):
            pass
        if not waiting:
            logger.info(f"{contextName}: Waiting for '{gpiomem}' is ready")
            waiting = True
        time.sleep(1)
    if waiting:
	    logger.info(f"{contextName}: Now '{gpiomem}' is ready")

#----------------------------------------
