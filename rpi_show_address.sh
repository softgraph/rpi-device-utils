#! /bin/bash

#---------------------------------------
# Show IP addresses of hosts.
#
# [USAGE]
#   - `./rpi_show_address.sh [OPTIONS]`
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
        if type dscacheutil > /dev/null 2>&1 ; then
            echo "--- ${host} ---"
            dscacheutil -q host -a name ${host} | grep -e 'address'
        fi
    fi
}

source rpi__main.sh
