from . import main

import datetime
import logging
import traceback

DEFAULT_TITLE      = "[tmonitor] Update"
DEFAULT_TITLE_WARN = "[tmonitor] Warning"
DEFAULT_TITLE_ERR  = "[tmonitor] Error"
DEFAULT_BODY       = "At {0} UTC the temperature is {1} C"

LOGGER = logging.getLogger(__name__)

def poll(query=None, notify=None, cond=None):
    time = datetime.datetime.now()
    try:
        temp = query()
    except:
        LOGGER.error("Could not query temperature")
        LOGGER.error(traceback.format_exc())
        notify.send(title=DEFAULT_TITLE_ERR, body=main.log.getvalue())
        return
    msg = DEFAULT_BODY.format(time, temp)
    LOGGER.info(msg)
    if cond is None:
        LOGGER.info("Sending update notification")
        notify.send(title=DEFAULT_TITLE, body=msg)
    elif cond(temp):
        LOGGER.info("Temperature exceeds boundary condition: sending warning notification")
        notify.send(title=DEFAULT_TITLE_WARN, body=msg)

