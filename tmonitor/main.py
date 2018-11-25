from . import monitor
from . import schedule
from . import temper

import argparse
import atexit
import io
import logging
import os.path
import re

LOGGER = logging.getLogger(__name__)

log = None

def main():
    # Setup batch logging (so that log output can be more finely controlled)
    global log
    log = io.StringIO()
    logging.basicConfig(stream=log, level=logging.INFO)
    atexit.register(lambda: print(log.getvalue()))
    # Parse command-line arguments
    args = parse_args()
    # Handle schedule list command
    if args['list']:
        schedule.list()
    # Handle scheduling poll
    elif args['hourly'] or \
            args['daily'] is not None or args['weekly'] is not None:
        schedule.add(args)
    # Handle non-scheduled poll
    else:
        # Initialize notifier
        if args['method'] == "email":
            notify = init_notify_email(args)
        else:
            LOGGER.error("Unknown notification method: {0}".format(args['method']))
            exit(1)
        # Parse notification condition
        if args['condition'] is not None:
            cond = parse_cond(args['condition'])
        else:
            cond = None
        # Poll the temperature monitor
        monitor.poll(query=temper.query, notify=notify, cond=cond)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Temperature Monitor", epilog="CONDITION := t (<|>) TEMP ((and|or) t (<|>) TEMP)*")
    parser.add_argument('-c', '--condition', help="Notification condition (see below)")
    gnotify = parser.add_argument_group("notification")
    gnotify.add_argument('-m', '--method', help="Notification method (only 'email' currently supported)")
    gnotify.add_argument('-s', '--source', help="Source address for use in notification")
    gnotify.add_argument('-d', '--destination', help="Destination address for use in notification")
    gnotify.add_argument('-t', '--host', help="Email server hostname")
    gnotify.add_argument('-r', '--port', help="Email server port on host")
    gnotify.add_argument('-f', '--credfile', type=os.path.abspath, help="Credentials file for use in notification")
    gnotify.add_argument('-u', '--user', help="Username for use in notification")
    gnotify.add_argument('-p', '--password', help="Password for use in notification")
    gschedule = parser.add_argument_group("scheduling")
    gschedule.add_argument('--boot', action='store_true', help="Schedule poll at system boot")
    gschedule.add_argument('--hourly', action='store_true', help="Schedule an hourly poll")
    gschedule.add_argument('--daily', type=int, metavar="HOUR", help="Schedule a daily poll at the given hour (24-hour format)")
    gschedule.add_argument('--weekly', type=int, metavar="DAY", help="Schedule a weekly poll on the given day (Sunday = 0)")
    gschedule.add_argument('-l', '--list', action='store_true', help="List currently scheduled polls")
    args = vars(parser.parse_args())
    return args

RE_COND = re.compile(r'^\s*(t\s*(<|>)\s*\d+)(\s*(and|or)\s+t\s*(<|>)\s*\d+)*\s*$')

def parse_cond(cond):
    if not RE_COND.match(cond):
        LOGGER.error("Invalid notification condition")
        exit(1)
    return lambda t: eval(cond, {'t': t})

def init_notify_email(args):
    """Initialize email notifier."""
    # Check that the necessary information was supplied for email config
    fail = False
    if args['source'] is None:
        LOGGER.error("No source address given for email")
        fail = True
    if args['destination'] is None:
        LOGGER.error("No destination address given for email")
        fail = True
    if args['host'] is None or args['port'] is None:
        LOGGER.error("Incomplete host/port pair given for email")
        fail = True
    if args['credfile'] is None and \
            (args['user'] is None or args['password'] is None):
        LOGGER.error("Incomplete authentication given for email")
        fail = True
    if fail:
        exit(1)
    # Configure email notifier
    from .notify import email
    notify = email.Notify(
        dst_addr=args['destination'],
        src_addr=args['source'],
        username=args['user'],
        password=args['password'],
        cred_file=args['credfile'],
        host=args['host'],
        port=args['port'],
    )
    return notify

if __name__=='__main__':
    main()

