#! /bin/bash

#---------------------------------------
# Show IP addresses of hosts.
#
# [USAGE]
#   - `./rpi_show_address.sh [OPTIONS] [TYPES]`
#
# [OPTIONS]
#   - `-s TARGETS_FILE`
#     or
#     `-t USER@HOSTNAME`
#   - If neither `-s` or `-t` is given, `targets` file is used instead.
#
# [TYPES]
#   - `inet`
#   - `inet6`
#   - `ether`
#   - `loop`
#   - `RX`
#   - `TX`
#   - If no type is given, `inet` is used instead.
#---------------------------------------

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -ge 1 ] ; then
        target=$1
        host=${target#*@}
        if [ $# -eq 2 ] ; then
            types=" $2 "
        elif [ $# -eq 3 ] ; then
            types=" $2 | $3 "
        elif [ $# -eq 4 ] ; then
            types=" $2 | $3 | $4 "
        elif [ $# -eq 5 ] ; then
            types=" $2 | $3 | $4 | $5 "
        elif [ $# -eq 6 ] ; then
            types=" $2 | $3 | $4 | $5 | $6 "
        elif [ $# -eq 7 ] ; then
            types=" $2 | $3 | $4 | $5 | $6 | $7 "
        else
            types=" inet "
        fi
        echo "--- ${host} ---"
        if ping -q -c 1 -t 1 ${host} | grep "1 packets received" > /dev/null 2>&1 ; then
            ssh ${target} "/usr/sbin/ifconfig | egrep ': flags=|$types'"
        fi
    fi
}

source rpi__main.sh
