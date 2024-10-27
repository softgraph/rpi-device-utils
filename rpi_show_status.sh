#! /bin/bash

# [USAGE]
# - `rpi_show_status.sh`
#   - Show statuses of `hosts`.
# - `rpi_show_status.sh -h HOSTNAME`
#   - Show statuses of HOSTNAME.

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 2 ]
    then
        host=$1
        user=$2
        echo "--- ${user}@${host} ---"
        for f in status.bash/*
        do
            if [ ! -f $f ] ; then continue ; fi
            cat $f | ssh ${user}@${host} bash
        done
    fi
}

source rpi__main.sh
