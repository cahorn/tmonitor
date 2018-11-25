`tmonitor`
==========

Daemon for scheduled, remote temperature monitoring.

Build
-----

`tmonitor` can be built via its python `setup.py` script.

    $ python3 setup.py install

### Dependencies

`tmonitor` built upon the Python 3 environment. Scheduling is performed via a
cron backend using the python module `python-crontab`, which is installed
automatically. It performs temperature queries through the
[`temper_query`](https://github.com/cahorn/temper-query) command, which must be
installed separately.

Basic Use
---------

As the underlying `temper_query` command requires root permission to directly
access the temperature sensor, all execution of the `tmonitor` program must also
occur with root permission.

To immediately poll the temperature and generate the appropriate notification:

    # tmonitor -m email -d DST -s SRC -t HOST -r PORT -u USER -p PWD

To do the same, but avoid explicitly typing your username and password at
execution time by storing them in a credentials file:

    # echo -e 'USER\nPWD' > FILE
    # tmonitor -m email -d DST -s SRC -t HOST -r PORT -f FILE

To schedule the same action to happen daily at 0600 hours:

    # tmonitor --daily 6 -m email -d DST -s SRC -t HOST -r PORT -f FILE

To schedule an hourly conditional notification if the temperature is below 15 C:

    # tmonitor --hourly -c 't < 15' -m email -d DST -s SRC -t HOST -r PORT -f FILE

To list all scheduled notifications:

    # tmonitor --list

To get a more comprehensive usage:

    # tmonitor --help

