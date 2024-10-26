#! /bin/bash

# [USAGE]
# - `rpi_ping.sh`
#   - Run `ping` to `hosts`.
# - `rpi_ping.sh HOST_1 HOST_2`
#   - Run `ping` to HOST_1 and HOST_2.

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 1 ] ; then
        host=$1
        echo "--- $1 ping ---"
        ping -c 3 -q $1 | grep -v -e '^$'
    fi
}

begin_proc

if [ $# -eq 0 ] ; then
    for i in `cat hosts` ; do
        do_proc $i
    done
else
    for i in $* ; do
        do_proc $i
    done
fi

end_proc
