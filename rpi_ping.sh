#! /bin/bash

# [USAGE]
# - `rpi_ping.sh`
#   - Run `ping` to `hosts`.
# - `rpi_ping.sh -h HOSTNAME`
#   - Run `ping` to HOSTNAME.

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -ge 1 ] ; then
        host=$1
        echo "--- $1 ping ---"
        ping -c 3 -q $1 | grep -v -e '^$'
    fi
}

source rpi__main.sh
