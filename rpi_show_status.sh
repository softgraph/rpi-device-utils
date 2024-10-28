#! /bin/bash

#---------------------------------------
# Show statuses of hosts.
#
# [USAGE]
#   - `./rpi_show_status.sh [OPTIONS]`
#
# [OPTIONS]
#   - `-t HOSTNAME`
#     or
#     `-t USER@HOSTNAME`
#   - If `-t` option is not specified, `targets` file is used instead.
#---------------------------------------

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 1 ]
    then
        target=$1
        echo "--- ${target} ---"
        for f in status.bash/*
        do
            if [ ! -f $f ] ; then continue ; fi
            cat $f | ssh ${target} bash
        done
    fi
}

source rpi__main.sh
