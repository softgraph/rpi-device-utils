#! /bin/bash

#---------------------------------------
# Run `ping` for hosts.
#
# [USAGE]
#   - `./rpi_ping.sh [OPTIONS]`
#
# [OPTIONS]
#   - `-s TAGETS_FILE`
#     or
#     `-t USER@HOSTNAME`
#   - If neither `-s` or `-t` is given, `targets` file is used instead.
#---------------------------------------

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 1 ] ; then
        target=$1
        host=${target#*@}
        echo "--- ${host} ping ---"
        ping -c 3 -q ${host} | grep -v -e '^$'
    fi
}

source rpi__main.sh
