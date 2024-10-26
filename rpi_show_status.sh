#! /bin/bash

# [USAGE]
# - `rpi_show_status.sh`
#   - Show statuses of `hosts`.
# - `rpi_show_status.sh HOST_1 HOST_2`
#   - Show statuses of HOST_1 and HOST_2.

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
        host=$1
        echo "--- ${host} ---"
        for f in status.bash/*
        do
            if [ ! -f $f ] ; then continue ; fi
            cat $f | ssh pi@${host} bash
        done
    fi
}

begin_proc

if [ $# -eq 0 ]
then
    for i in `cat hosts`
    do
        do_proc $i
    done
else
    for i in $*
    do
        do_proc $i
    done
fi

end_proc
