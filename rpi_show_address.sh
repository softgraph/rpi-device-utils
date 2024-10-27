#! /bin/bash

# [USAGE]
# - `rpi_show_address.sh`
#   - Show IP addresses of `hosts`.
# - `rpi_show_address.sh -h HOSTNAME`
#   - Show IP addresses of HOSTNAME.

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
        if type dscacheutil > /dev/null 2>&1 ; then
            echo "--- ${host} ---"
            dscacheutil -q host -a name ${host} | grep -e 'address'
        fi
    fi
}

source rpi__main.sh
