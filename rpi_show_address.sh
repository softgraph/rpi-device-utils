#! /bin/bash

# [USAGE]
# - `rpi_show_address.sh`
#   - Show IP addresses of `hosts`.
# - `rpi_show_address.sh HOST_1 HOST_2`
#   - Show IP addresses of HOST_1 and HOST_2.

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
        if type dscacheutil > /dev/null 2>&1 ; then
            echo "--- ${host} ---"
            dscacheutil -q host -a name ${host} | grep -e 'address'
        fi
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
