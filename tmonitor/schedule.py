import datetime
import crontab
import re

cron = crontab.CronTab(user=True)

def add(args):
    """Add a new monitor poll to the schedule."""
    # Construct monitor poll command
    cmd_args = ['/usr/local/bin/tmonitor']
    for flag, arg in args.items():
        if flag not in ['boot', 'hourly', 'daily', 'weekly', 'list'] \
                and arg is not None:
            cmd_args.append("--{0}".format(flag))
            cmd_args.append("'{0}'".format(arg))
    cmd_args.append('| logger -t tmonitor')
    command = " ".join(cmd_args)
    # Construct an identifiable comment
    comment = "[tmonitor] {0}".format(datetime.datetime.now())
    # Schedule the new poll
    job = cron.new(command=command, comment=comment)
    if args['weekly'] is not None:
        job.dow.on(args['weekly'])
    if args['daily'] is not None:
        job.hour.on(args['daily'])
    if args['hourly']:
        job.minute.on(0)
    if args['boot']:
        job.every_reboot()
    cron.write()

def list():
    """List all scheduled monitor polls."""
    for job in cron:
        if job.comment.startswith("[tmonitor]"):
            print(job)

